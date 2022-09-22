
from ..hydraulics.consumptions import compute_pressure_fractions, compute_regularized_unitary_consumptions, \
    compute_consumptions, compute_regularized_unitary_consumption_derivatives_with_respect_to_heads, \
    compute_consumption_derivatives_with_respect_to_heads
from ..hydraulics.friction_headlosses import compute_regularized_friction_headlosses_until_x, \
    compute_regularized_friction_headloss_derivatives_with_respect_to_flows_until_x

from ..solvers import compute_headlosses_from_source_nodes, compute_energy_residuals_in_pipes, \
    compute_mass_residuals_at_junctions, SolverException, SolverWarning

import numpy as np
from scipy import sparse
from scipy.sparse import linalg

import warnings
import math


ABSOLUTE_TOLERANCE_ON_NULL_RESIDUAL = 1e-3
"""Absolute tolerance on null residuals, under which we consider a hydraulic solution may have been reached"""

RELATIVE_TOLERANCE_BETWEEN_TWO_NEWTON_STEPS = 1e-6
"""Relative tolerance on residuals or iterates between two consecutive Newton's steps, under which we consider a 
hydraulic solution may have been reached"""

NEWTON_MAXIMUM_ITERATION_NUMBER = 1e2
"""Maximum number of iterations to solve the system with the Newton's method at each hydraulic time step"""

MAXIMUM_MAGNITUDE_ORDER_BETWEEN_DERIVATIVES_AFTER_REGULARIZATION = 1e10
"""Number of magnitude orders of difference between the derivatives from which derivatives will be regularized to 
improve the conditioning of the Jacobian matrix"""

GOLDSTEIN_INDEX_LOWER_LIMIT = 0.1
"""Lower limit of the Goldstein index used for damping, and upper which we consider the line search did_succeed in 
finding the correct value of the current Newton's method iterate 
"""

GOLDSTEIN_DECREASING_STEP_SIZE_MULTIPLIER = 0.5
"""Multiplier used to decrease the step size in the Goldstein's step size selection algorithm used for damping"""

MAXIMUM_NUMBER_OF_DAMPING_CORRECTIONS = 10
"""Maximum number of corrections to apply on the descents during the line search used to find each Newton's iterate with 
damping"""

ABSOLUTE_TOLERANCE_ON_LINE_SEARCH_DIRECTION = 1e-12
"""absolute tolerance on reduced Goldstein index denominator under which we consider the hydraulic there is no possible 
descent and that there is not anymore justified iteration"""


class NewtonException(SolverException):
    """
    Base class for any exception raised from current package.
    """
    pass


class NewtonWarning(SolverWarning):
    """
    Base class for any exception raised from current package.
    """
    pass


def solve_balance_equations(
        previous_flows, previous_heads_at_junctions, fixed_demands_at_junctions, fixed_heads_at_tanks,
        fixed_parameters):
    """
    Solve the hydraulic PDM balance equation for given fixed demands and heads at tanks, and return new computed
    flows, heads at junctions, solver status, solver metrics, and error messages.

    Uses hybrid Newton's method, i.e. Newton's method on the reduced Lagrangian, with, at each Newton's iteration,
    a damping algorithm which stops when the weighted least square of the residuals are found.

    :param previous_flows: flows at previous time step
    :param previous_heads_at_junctions: heads at junctions at previous time step
    :param fixed_demands_at_junctions: demands at current time step
    :param fixed_heads_at_tanks: heads at tanks at current time step
    :param fixed_parameters: dictionary containing fixed parameters needed by the solver ; keys are: 'number_of_pipes',
    'heads_at_reservoirs', 'incidence_matrix_reduced_to_tanks', 'incidence_matrix_reduced_to_reservoirs',
    'number_of_junctions', 'max_head_at_reservoirs', 'junction_elevations',
    'unitary_consumption_regularization_close_to_zero', 'unitary_consumption_regularization_close_to_one',
    'friction_coefficients', 'pipe_lengths', 'reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero',
    'incidence_matrix_reduced_to_junctions', 'unitary_consumption_derivative_regularization_close_to_zero',
    'unitary_consumption_derivative_regularization_close_to_one', 'pressure_fraction_derivative',
    'reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero'
    :return: new_flows, new_heads_at_junctions, solver status (True if succeeded, False otherwise), solver metrics,
    and error messages
    """
    # retrieve needed fixed parameters
    (number_of_pipes, heads_at_reservoirs, incidence_matrix_reduced_to_tanks, incidence_matrix_reduced_to_reservoirs,
     number_of_junctions, max_head_at_reservoirs) \
        = (fixed_parameters[key] for key
           in ['number_of_pipes', 'heads_at_reservoirs', 'incidence_matrix_reduced_to_tanks',
               'incidence_matrix_reduced_to_reservoirs', 'number_of_junctions', 'max_head_at_reservoirs'])
    # compute headlosses from source nodes, and diagonal matrix of weights
    fixed_headlosses_from_source_nodes = compute_headlosses_from_source_nodes(
        number_of_pipes, fixed_heads_at_tanks, heads_at_reservoirs, incidence_matrix_reduced_to_tanks,
        incidence_matrix_reduced_to_reservoirs)
    residuals_weighting_matrix = _compute_residuals_weighting_matrix(
        number_of_pipes, fixed_demands_at_junctions, fixed_heads_at_tanks, max_head_at_reservoirs)
    fixed_parameters.update({'residuals_weighting_matrix': residuals_weighting_matrix})
    # set starting estimates, initial residuals, and other variables needed in the algorithm's loop
    q0, h0 = previous_flows, previous_heads_at_junctions  # starting estimates of iterates
    allres0 = np.zeros(number_of_pipes + number_of_junctions, dtype=float)  # initial energy residuals
    q, h = None, None  # current iterates
    allres = None
    k = 0  # iteration counter
    res_diffs = {}  # residual differences between each previous and current iterations (for conv. order too)
    itervars = {}  # current variables stored to prevent from recomputing variables
    error_messages = []  # list to store error messages
    did_succeed = False  # initial status of the solver

    # iterate until a "break"
    while True:
        try:
            # compute next Newton's iterates
            q, h = _compute_next_newton_iterates(
                q0, h0, fixed_demands_at_junctions, fixed_headlosses_from_source_nodes, fixed_parameters, itervars)
        except NewtonException as e:
            e_str = str(e)
            if k == 0:
                # exception raised at first iteration ; then there is not any computed value to use as
                # partial-convergence state ; thus, store the error message and re-raise an exception to stop
                # execution
                condition_number = compute_jacobian_schur_complement_matrix_condition_number(
                    previous_flows, previous_heads_at_junctions, fixed_demands_at_junctions, fixed_parameters)
                error_message = "An exception was raised at first iteration of the Newton's algorithm ({}) ; " \
                                "condition number of the Jacobian matrix is {}.".format(e_str, condition_number)
                error_messages.append(error_message)
                raise NewtonException(error_messages)
            # if we are here, then it means that it's not the first iteration ; thus, we can use last computed
            # values as partial-convergence state, issue a warning, and break
            error_messages.append(e_str)
            warnings.warn(e_str, NewtonWarning)
            break
        # compute stop criterion
        eres, mres = itervars['energy_residuals'], itervars['mass_residuals']
        allres = np.concatenate([eres, mres])
        res_norm_inf = np.linalg.norm(allres, ord=np.inf)
        is_residuals_stop_criterion_satisfied = res_norm_inf < ABSOLUTE_TOLERANCE_ON_NULL_RESIDUAL
        is_iterates_stop_criterion_satisfied = True
        for prev_iter, new_iter in ((q0, q), (h0, h)):
            is_iterates_stop_criterion_satisfied &= is_gradients_stop_criterion_satisfied(prev_iter, new_iter)
        # test for convergence from computed criteria
        if is_residuals_stop_criterion_satisfied & is_iterates_stop_criterion_satisfied:
            # it converged ; then...
            # ... set success flag to True ...
            did_succeed = True
            # ... and stop
            break
        # did not break ; thus...
        # ... increment number of iterations ...
        k += 1
        # ... compute and store residual differences for later use ...
        curr_res_diff = allres - allres0
        res_diffs[k] = curr_res_diff
        # ... test if max number of iterations is reached...
        if k >= NEWTON_MAXIMUM_ITERATION_NUMBER:
            # it is reached ; then issue a warning...
            res_diff_inf_norm = np.linalg.norm(curr_res_diff, ord=np.inf)
            iter_diff_inf_norm = np.linalg.norm(np.concatenate([q - q0, h - h0]), ord=np.inf)
            error_message = \
                "Newton's algorithm did not converge after {} iterations. Inf. norm between last two computed " \
                "residues is: {}. Inf. norm between last two computed iterates is: {}.".format(
                    NEWTON_MAXIMUM_ITERATION_NUMBER, res_diff_inf_norm, iter_diff_inf_norm)
            warnings.warn(error_message, NewtonWarning)
            error_messages.append(error_message)
            # ... and break
            break
        else:
            # max number of iterations is not reached ; then...
            # ... update iteration variables...
            q0 = q
            h0 = h
            allres0 = allres
            # ... and continue to next iteration

    # solver metrics
    solver_metrics = {'residuals': allres,
                      'number_of_iterations': k, 'res_diffs_per_iteration': res_diffs,
                      'number_of_damping_corrections': itervars['number_of_damping_corrections']}

    return q, h, did_succeed, solver_metrics, error_messages


def _compute_next_newton_iterates(
        previous_flows, previous_heads_at_junctions, fixed_demands_at_junctions, fixed_headlosses_from_source_nodes,
        fixed_parameters, iteration_variables_to_reuse):
    """
    Compute next Newton's iterates, using Newton's hybrid algorithm (a.k.a Newton applied to reduced Lagrangian), as
    in Piller et al. (2003). Return new flows and new heads at junctions, and update in-place dictionary
    `iteration_variables_to_reuse`.

    :param previous_flows: flows of previous Newton's iteration
    :param previous_heads_at_junctions: heads at junctions from previous Newton's iteration
    :param fixed_demands_at_junctions: demands at junctions for current time step
    :param fixed_headlosses_from_source_nodes: contribution of sources nodes (i.e. tanks and reservoirs) in the
    resulting headlosses along pipes
    :param fixed_parameters: dictionary of needed fixed parameters ; keys are: 'junction_elevations',
    'unitary_consumption_regularization_close_to_zero', 'unitary_consumption_regularization_close_to_one',
    'friction_coefficients', 'pipe_lengths', 'reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero',
    'incidence_matrix_reduced_to_junctions', 'residuals_weighting_matrix',
    'unitary_consumption_derivative_regularization_close_to_zero',
    'unitary_consumption_derivative_regularization_close_to_one', 'pressure_fraction_derivative',
    'reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero'
    :param iteration_variables_to_reuse: dictionary of iteration variables computed at previous call of function
    `_compute_next_newton_iterates` for the same time step, and which need to be updated in-place for reuse at next time
    step ; if not empty, then it must contain following keys (and their associated values): 'energy_residuals',
    'mass_residuals', 'residuals_weighted_least_square', 'line_search_direction', 'pressure_fractions' and
    'number_of_damping_corrections' ; if empty, then it means that this is the first Newton's iteration of current time
    step, and that the variables associated to all these keys need to be computed or initialized ; in short terms: this
    dictionary prevents from recomputing already computed variables
    :return: next Newton's iterates, consisting in new flows and new heads at junctions
    """
    # retrieve fixed parameters passed as arguments to the function
    (junction_elevations, unitary_consumption_regularization_close_to_zero,
     unitary_consumption_regularization_close_to_one, friction_coefficients, pipe_lengths,
     reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero, incidence_matrix_reduced_to_junctions,
     residuals_weighting_matrix, unitary_consumption_derivative_regularization_close_to_zero,
     unitary_consumption_derivative_regularization_close_to_one, pressure_fraction_derivative,
     reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero) \
        = (fixed_parameters[key] for key
           in ['junction_elevations', 'unitary_consumption_regularization_close_to_zero',
               'unitary_consumption_regularization_close_to_one', 'friction_coefficients', 'pipe_lengths',
               'reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero',
               'incidence_matrix_reduced_to_junctions', 'residuals_weighting_matrix',
               'unitary_consumption_derivative_regularization_close_to_zero',
               'unitary_consumption_derivative_regularization_close_to_one', 'pressure_fraction_derivative',
               'reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero'])

    if len(iteration_variables_to_reuse) == 0:
        # it is the first call to the function for current time step (i.e. first Newton's iteration): compute everything
        previous_pressure_fractions = compute_pressure_fractions(previous_heads_at_junctions, junction_elevations)
        previous_unitary_consumptions = compute_regularized_unitary_consumptions(
            previous_pressure_fractions, unitary_consumption_regularization_close_to_zero,
            unitary_consumption_regularization_close_to_one)
        previous_consumptions = compute_consumptions(previous_unitary_consumptions, fixed_demands_at_junctions)
        previous_friction_headlosses = compute_regularized_friction_headlosses_until_x(
            previous_flows, friction_coefficients, pipe_lengths,
            reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero)
        previous_energy_residuals = compute_energy_residuals_in_pipes(
            previous_friction_headlosses, previous_heads_at_junctions, fixed_headlosses_from_source_nodes,
            incidence_matrix_reduced_to_junctions)
        previous_mass_residuals = compute_mass_residuals_at_junctions(
            previous_flows, previous_consumptions, incidence_matrix_reduced_to_junctions)
        previous_residuals = np.concatenate([previous_energy_residuals, previous_mass_residuals])
        previous_residuals_weighted_least_square = _compute_weighted_least_square_of_residuals(
            previous_residuals, residuals_weighting_matrix)
        previous_line_search_direction = 2 * previous_residuals_weighted_least_square
        iteration_variables_to_reuse.update(
            {'energy_residuals': previous_energy_residuals, 'mass_residuals': previous_mass_residuals,
             'residuals_weighted_least_square': previous_residuals_weighted_least_square,
             'line_search_direction': previous_line_search_direction, 'pressure_fractions': previous_pressure_fractions,
             'number_of_damping_corrections': 0})
    else:
        # it is not the first call to the function for current time step ; reused previously computed values
        previous_energy_residuals = iteration_variables_to_reuse['energy_residuals']
        previous_mass_residuals = iteration_variables_to_reuse['mass_residuals']
        previous_residuals_weighted_least_square = iteration_variables_to_reuse['residuals_weighted_least_square']
        previous_line_search_direction = iteration_variables_to_reuse['line_search_direction']
        previous_pressure_fractions = iteration_variables_to_reuse['pressure_fractions']
    if math.isclose(previous_line_search_direction, 0, abs_tol=ABSOLUTE_TOLERANCE_ON_LINE_SEARCH_DIRECTION):
        # we reach an extremum or a saddle point: no further iteration is justified
        new_flows = previous_flows
        new_heads_at_junctions = previous_heads_at_junctions
    elif previous_line_search_direction < 0:
        raise NewtonException('Ascent direction computed ; residuals weighted least squares = {}'.format(
            previous_residuals_weighted_least_square))
    else:
        # compute new descents
        unitary_consumption_derivatives = compute_regularized_unitary_consumption_derivatives_with_respect_to_heads(
            previous_pressure_fractions, unitary_consumption_derivative_regularization_close_to_zero,
            unitary_consumption_derivative_regularization_close_to_one, pressure_fraction_derivative)
        consumption_derivatives = compute_consumption_derivatives_with_respect_to_heads(
            unitary_consumption_derivatives, fixed_demands_at_junctions)
        friction_headloss_derivatives = compute_regularized_friction_headloss_derivatives_with_respect_to_flows_until_x(
            previous_flows, friction_coefficients, pipe_lengths,
            reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero)
        friction_headloss_derivatives, consumption_derivatives = _regularize_ill_conditioned_derivatives(
            friction_headloss_derivatives, consumption_derivatives)
        inverse_of_friction_headloss_derivatives_diagonal_matrix = sparse.diags(1 / friction_headloss_derivatives)
        consumption_derivatives_diagonal_matrix = sparse.diags(consumption_derivatives)
        jacobian_schur_complement_matrix = _compute_jacobian_schur_complement_matrix(
            inverse_of_friction_headloss_derivatives_diagonal_matrix, consumption_derivatives_diagonal_matrix,
            incidence_matrix_reduced_to_junctions)
        inverse_of_friction_headloss_derivatives_diagonal_matrix = sparse.diags(1 / friction_headloss_derivatives)
        rhs_to_compute_descents_of_heads_at_junctions = \
            - previous_mass_residuals - incidence_matrix_reduced_to_junctions \
            @ inverse_of_friction_headloss_derivatives_diagonal_matrix @ previous_energy_residuals
        descents_of_heads_at_junctions = linalg.spsolve(
            jacobian_schur_complement_matrix, rhs_to_compute_descents_of_heads_at_junctions, use_umfpack=True)
        descents_of_flows = \
            inverse_of_friction_headloss_derivatives_diagonal_matrix \
            @ (- previous_energy_residuals + incidence_matrix_reduced_to_junctions.T
               @ descents_of_heads_at_junctions)
        # compute new undamped iterates
        new_undamped_flows = previous_flows + descents_of_flows
        new_undamped_heads_at_junctions = previous_heads_at_junctions + descents_of_heads_at_junctions
        _update_iteration_variables_to_reuse(
            new_undamped_flows, new_undamped_heads_at_junctions, fixed_demands_at_junctions,
            fixed_headlosses_from_source_nodes, fixed_parameters, iteration_variables_to_reuse)
        new_residuals_weighted_least_square = iteration_variables_to_reuse['residuals_weighted_least_square']
        goldstein_index = _compute_goldstein_index(
            previous_residuals_weighted_least_square, new_residuals_weighted_least_square,
            previous_line_search_direction)
        if goldstein_index < GOLDSTEIN_INDEX_LOWER_LIMIT:
            # apply damping on descents to find better iterates
            new_flows, new_heads_at_junctions = _apply_damping_on_descents(
                previous_flows, previous_heads_at_junctions, descents_of_flows, descents_of_heads_at_junctions,
                previous_residuals_weighted_least_square, previous_line_search_direction, fixed_demands_at_junctions,
                fixed_headlosses_from_source_nodes, fixed_parameters, iteration_variables_to_reuse)
        else:
            # no damping is needed
            new_flows, new_heads_at_junctions = new_undamped_flows, new_undamped_heads_at_junctions
    return new_flows, new_heads_at_junctions


def is_gradients_stop_criterion_satisfied(x0, x):
    """
    Stop criterion based on inf. norm of global differences between values of last two steps, as in Elhay et al.
    (2016) ; also includes an absolute tolerance term.

    :param x0: previous step values
    :param x: current step values
    :return: True if the criterion is satisfied, False otherwise
    """
    x_or_res_norm_inf = np.linalg.norm(x, ord=np.inf)
    if x_or_res_norm_inf == 0:
        x_or_res_norm_inf = 1
    is_gradients_global_stop_criterion_satisfied = \
        np.linalg.norm(x - x0, ord=np.inf) / x_or_res_norm_inf < RELATIVE_TOLERANCE_BETWEEN_TWO_NEWTON_STEPS
    return is_gradients_global_stop_criterion_satisfied


def _apply_damping_on_descents(
        previous_flows, previous_heads_at_junctions, descents_of_flows, descents_of_heads_at_junctions,
        previous_residuals_weighted_least_square, previous_line_search_direction, fixed_demands_at_junctions,
        fixed_headlosses_from_source_nodes, fixed_parameters, iteration_variables_to_reuse):
    """
    Apply damping (a.k.a. step-size control) on Newton's descents using Goldstein's line search algorithm on the
    Weighted Least Squares (WLS) formulation (Elhay et al., 2016) to find better iterates

    :param previous_flows: flows at previous Newton's iteration
    :param previous_heads_at_junctions: heads at junctions at previous Newton's iteration
    :param descents_of_flows: descents of flows for current Newton's iteration
    :param descents_of_heads_at_junctions: descents of heads at junctions for current Newton's iteration
    :param previous_residuals_weighted_least_square: weighted least square of residuals computed at previous Newton's
    iteration
    :param previous_line_search_direction: direction of the line search computed at previous Newton's iteration
    :param fixed_demands_at_junctions: demands at junctions at current time step
    :param fixed_headlosses_from_source_nodes: contribution of sources (i.e. tanks and reservoirs) nodes in the
    resulting headlosses along pipes for current time step
    :param fixed_parameters: dictionary of needed fixed parameters ; keys are: 'junction_elevations',
    'unitary_consumption_regularization_close_to_zero', 'unitary_consumption_regularization_close_to_one',
    'friction_coefficients', 'pipe_lengths', 'reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero',
    'incidence_matrix_reduced_to_junctions', 'residuals_weighting_matrix'
    :param iteration_variables_to_reuse: dictionary of variables to reused from previous Newton's iteration and to
    update in-place
    :return: new damped flows and heads at junctions
    """
    number_of_damping_corrections = 1
    step_size = GOLDSTEIN_DECREASING_STEP_SIZE_MULTIPLIER
    while True:
        new_damped_flows = previous_flows + step_size * descents_of_flows
        new_damped_heads_at_junctions = previous_heads_at_junctions + step_size * descents_of_heads_at_junctions
        _update_iteration_variables_to_reuse(
            new_damped_flows, new_damped_heads_at_junctions, fixed_demands_at_junctions,
            fixed_headlosses_from_source_nodes, fixed_parameters, iteration_variables_to_reuse)
        new_residuals_weighted_least_square = iteration_variables_to_reuse['residuals_weighted_least_square']
        goldstein_index = _compute_goldstein_index(
            previous_residuals_weighted_least_square, new_residuals_weighted_least_square,
            previous_line_search_direction, step_size)
        if goldstein_index >= GOLDSTEIN_INDEX_LOWER_LIMIT:
            break
        elif number_of_damping_corrections >= MAXIMUM_NUMBER_OF_DAMPING_CORRECTIONS:
            raise NewtonException(
                "Max number of damping iterations reached ({}), but goldstein index = {}.".format(
                    MAXIMUM_NUMBER_OF_DAMPING_CORRECTIONS, goldstein_index))
        else:
            step_size *= GOLDSTEIN_DECREASING_STEP_SIZE_MULTIPLIER
            number_of_damping_corrections += 1
    iteration_variables_to_reuse['number_of_damping_corrections'] += number_of_damping_corrections
    return new_damped_flows, new_damped_heads_at_junctions


def _compute_residuals_weighting_matrix(
        number_of_pipes, fixed_demands_at_junctions, fixed_heads_at_tanks=None, max_head_at_reservoirs=None):
    """
    Compute the diagonal matrix of positive weights to apply on residuals at each Newton's iteration.
    These weights account for significant differences in scale between heads and flows, and are computed as in Elhay
    et al. (2016), dividing energy and mass residuals by respectively the maximum head among the fixed-head nodes
    (i.e. tanks and reservoirs) and the maximum demand at junctions. Upper left elements of the diagonal matrix will
    apply on squared energy residuals, and lower right elements will apply on squared mass residuals.

    Note: if, at a given time step, all demands are 0, then the weighting matrix to apply on the mass residuals is
    the unity matrix.

    :param number_of_pipes: number of pipes
    :param fixed_demands_at_junctions: demands at junctions at current time step (l/s)
    :param fixed_heads_at_tanks: heads at tanks at current time step (mH2O)
    :param max_head_at_reservoirs: the maximum head at reservoirs (mH2O)
    :return: diagonal matrix of positive weights
    """
    max_head_at_sources = -np.inf
    if max_head_at_reservoirs is not None:
        max_head_at_sources = max_head_at_reservoirs
    if fixed_heads_at_tanks is not None:
        max_head_at_sources = max(fixed_heads_at_tanks.max(), max_head_at_sources)
    if max_head_at_sources in (-np.inf, 0):
        max_head_at_sources = 1
    energy_residuals_weighting = 1 / max_head_at_sources ** 2
    energy_residuals_weighting_diagonal = np.full(number_of_pipes, energy_residuals_weighting, dtype=float)
    energy_residuals_residuals_weighting_matrix = sparse.diags(energy_residuals_weighting_diagonal)

    max_demands_at_junctions = fixed_demands_at_junctions.max()
    if max_demands_at_junctions == 0:
        max_demands_at_junctions = 1
    mass_residuals_weighting = 1 / max_demands_at_junctions ** 2
    mass_residuals_weighting_diagonal = np.full_like(fixed_demands_at_junctions, mass_residuals_weighting)
    mass_residuals_residuals_weighting_matrix = sparse.diags(mass_residuals_weighting_diagonal)

    residuals_weighting_matrix = sparse.block_diag(
        [energy_residuals_residuals_weighting_matrix, mass_residuals_residuals_weighting_matrix])

    return residuals_weighting_matrix


def _compute_weighted_least_square_of_residuals(all_residuals, residuals_weighting_matrix):
    """
    Compute the weighted least square of the residuals.

    :param all_residuals: a vector obtained from the concatenation of both energy and mass residuals
    :param residuals_weighting_matrix: diagonal matrix of positive weights to apply on residuals
    :return: the weighted least square of the residuals (scalar)
    """
    return 0.5 * all_residuals.T @ residuals_weighting_matrix @ all_residuals


def _regularize_ill_conditioned_derivatives(friction_headloss_derivatives, consumption_derivatives):
    """
    Regularize ill-conditioned derivatives in the Jacobian matrix, thresholding them so they can't differ from each
    other by more than `MAXIMUM_MAGNITUDE_ORDER_BETWEEN_DERIVATIVES_AFTER_REGULARIZATION` magnitude orders, as in Elhay
    et al. (2011)

    :param friction_headloss_derivatives: potentially ill-conditioned friction headloss derivatives
    :param consumption_derivatives: potentially ill-conditioned friction consumption derivatives
    :return: regularized friction headloss and consumption derivatives
    """
    dy = np.concatenate([friction_headloss_derivatives, consumption_derivatives])
    dy_abs = np.abs(dy)
    dy_abs_min = dy_abs.max() / MAXIMUM_MAGNITUDE_ORDER_BETWEEN_DERIVATIVES_AFTER_REGULARIZATION
    dy_abs[dy_abs < dy_abs_min] = dy_abs_min
    dy_reg = np.copysign(dy_abs, dy)
    number_of_pipes = len(friction_headloss_derivatives)
    friction_headloss_derivatives_regularized = dy_reg[:number_of_pipes]
    consumption_derivatives_regularized = dy_reg[number_of_pipes:]
    return friction_headloss_derivatives_regularized, consumption_derivatives_regularized


def compute_jacobian_schur_complement_matrix_condition_number(
        previous_flows, previous_heads_at_junctions, fixed_demands_at_junctions, fixed_parameters):
    """
    Compute the condition number of the Schur complement of the Jacobian matrix

    :param previous_flows: flows computed at previous Newton's iteration
    :param previous_heads_at_junctions: heads at junctions computed at previous Newton's iteration
    :param fixed_demands_at_junctions: demands at junctions for current time step
    :param fixed_parameters: dictionary of needed fixed parameters ; keys are: 'junction_elevations',
    'friction_coefficients', 'pipe_lengths', 'incidence_matrix_reduced_to_junctions',
    'unitary_consumption_derivative_regularization_close_to_zero',
    'unitary_consumption_derivative_regularization_close_to_one', 'pressure_fraction_derivative',
    'reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero'
    :return: the condition number of the Schur complement of the Jacobian matrix
    """
    (junction_elevations, friction_coefficients, pipe_lengths, incidence_matrix_reduced_to_junctions,
     unitary_consumption_derivative_regularization_close_to_zero,
     unitary_consumption_derivative_regularization_close_to_one, pressure_fraction_derivative,
     reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero) \
        = (fixed_parameters[key] for key
           in ['junction_elevations', 'friction_coefficients', 'pipe_lengths', 'incidence_matrix_reduced_to_junctions',
               'unitary_consumption_derivative_regularization_close_to_zero',
               'unitary_consumption_derivative_regularization_close_to_one', 'pressure_fraction_derivative',
               'reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero'])
    friction_headloss_derivatives = compute_regularized_friction_headloss_derivatives_with_respect_to_flows_until_x(
        previous_flows, friction_coefficients, pipe_lengths,
        reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero)
    inverse_of_friction_headloss_derivatives_diagonal_matrix = sparse.diags(1 / friction_headloss_derivatives)
    pressure_fractions = compute_pressure_fractions(previous_heads_at_junctions, junction_elevations)
    unitary_consumption_derivatives = compute_regularized_unitary_consumption_derivatives_with_respect_to_heads(
        pressure_fractions, unitary_consumption_derivative_regularization_close_to_zero,
        unitary_consumption_derivative_regularization_close_to_one, pressure_fraction_derivative)
    consumption_derivatives = compute_consumption_derivatives_with_respect_to_heads(
        unitary_consumption_derivatives, fixed_demands_at_junctions)
    consumption_derivatives_diagonal_matrix = sparse.diags(consumption_derivatives)
    jacobian_schur_complement_matrix = _compute_jacobian_schur_complement_matrix(
        inverse_of_friction_headloss_derivatives_diagonal_matrix, consumption_derivatives_diagonal_matrix,
        incidence_matrix_reduced_to_junctions)
    condition_number = np.linalg.cond(jacobian_schur_complement_matrix.todense())
    return condition_number


def _update_iteration_variables_to_reuse(
        new_flows, new_heads_at_junctions, fixed_demands_at_junctions, fixed_headlosses_from_source_nodes,
        fixed_parameters, iteration_variables_to_update):
    """
    Update variables in dictionary `iteration_variables_to_update` in-place

    :param new_flows: new flows iterate
    :param new_heads_at_junctions: new heads at junctions iterate
    :param fixed_demands_at_junctions: current demands at junctions
    :param fixed_headlosses_from_source_nodes: contribution of sources (i.e. tanks and reservoirs) nodes in the
    resulting headlosses along pipes
    :param fixed_parameters: dictionary of needed fixed parameters ; keys are: 'junction_elevations',
    'unitary_consumption_regularization_close_to_zero', 'unitary_consumption_regularization_close_to_one',
    'friction_coefficients', 'pipe_lengths', 'reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero',
    'incidence_matrix_reduced_to_junctions', 'residuals_weighting_matrix'
    :param iteration_variables_to_update: dictionary of iteration variables to update in-place, and which keys are
    'energy_residuals', 'mass_residuals', 'residuals_weighted_least_square', 'line_search_direction' and
    'pressure_fractions'
    """
    (junction_elevations, unitary_consumption_regularization_close_to_zero,
     unitary_consumption_regularization_close_to_one, friction_coefficients, pipe_lengths,
     reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero, incidence_matrix_reduced_to_junctions,
     residuals_weighting_matrix) \
        = (fixed_parameters[key] for key
           in ['junction_elevations', 'unitary_consumption_regularization_close_to_zero',
               'unitary_consumption_regularization_close_to_one', 'friction_coefficients', 'pipe_lengths',
               'reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero',
               'incidence_matrix_reduced_to_junctions', 'residuals_weighting_matrix'])
    new_friction_headlosses = compute_regularized_friction_headlosses_until_x(
        new_flows, friction_coefficients, pipe_lengths,
        reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero)
    new_energy_residuals = compute_energy_residuals_in_pipes(
        new_friction_headlosses, new_heads_at_junctions, fixed_headlosses_from_source_nodes,
        incidence_matrix_reduced_to_junctions)
    new_pressure_fractions = compute_pressure_fractions(new_heads_at_junctions, junction_elevations)
    new_unitary_consumptions = compute_regularized_unitary_consumptions(
        new_pressure_fractions, unitary_consumption_regularization_close_to_zero,
        unitary_consumption_regularization_close_to_one)
    new_consumptions = compute_consumptions(new_unitary_consumptions, fixed_demands_at_junctions)
    new_mass_residuals = compute_mass_residuals_at_junctions(
        new_flows, new_consumptions, incidence_matrix_reduced_to_junctions)
    new_residuals = np.concatenate([new_energy_residuals, new_mass_residuals])
    new_residuals_weighted_least_square = _compute_weighted_least_square_of_residuals(
        new_residuals, residuals_weighting_matrix)
    new_line_search_direction = 2 * new_residuals_weighted_least_square
    iteration_variables_to_update.update(
        {'energy_residuals': new_energy_residuals, 'mass_residuals': new_mass_residuals,
         'residuals_weighted_least_square': new_residuals_weighted_least_square,
         'line_search_direction': new_line_search_direction, 'pressure_fractions': new_pressure_fractions})


def _compute_jacobian_schur_complement_matrix(
        inverse_of_friction_headloss_derivatives_diagonal_matrix, consumption_derivatives_diagonal_matrix, 
        incidence_matrix_reduced_to_junctions):
    """
    Compute the Schur complement of the Jacobian matrix

    :param inverse_of_friction_headloss_derivatives_diagonal_matrix: diagonal matrix with inverse of friction
    headloss derivatives on its diagonal
    :param consumption_derivatives_diagonal_matrix: diagonal matrix with consumption derivatives on its diagonal
    :param incidence_matrix_reduced_to_junctions: incidence matrix reduced to junctions
    :return: the Schur complement of the Jacobian matrix
    """
    jacobian_schur_complement_matrix = \
        - incidence_matrix_reduced_to_junctions @ inverse_of_friction_headloss_derivatives_diagonal_matrix \
        @ incidence_matrix_reduced_to_junctions.T - consumption_derivatives_diagonal_matrix
    return jacobian_schur_complement_matrix


def _compute_goldstein_index(
        previous_residuals_weighted_least_square, new_residuals_weighted_least_square, previous_line_search_direction,
        step_size=1.0):
    """
    Compute Goldstein's index.

    :param previous_residuals_weighted_least_square: weighted least square of the residuals computed at previous
    Newton's iteration
    :param new_residuals_weighted_least_square: weighted least square of the residuals computed from new values of flows
    and heads at junctions
    :param step_size: step size of the damp which has been applied on the descents used to compute the new values of the
    flows and heads at junctions ; default is `1.0`, which means that no damping was applied on the descents
    :return: Goldstein's index (scalar ; unitless)
    """
    goldstein_index = \
        (previous_residuals_weighted_least_square - new_residuals_weighted_least_square) \
        / (step_size * previous_line_search_direction)
    return goldstein_index
