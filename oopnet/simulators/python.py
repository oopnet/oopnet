"""Front-end to initialize and run a Extended Period Simulation (EPS) with Pressure Driven Model (PDM) of consumptions.
"""

from __future__ import annotations
import datetime
import os
import uuid
import shutil
from typing import Union, Optional, TYPE_CHECKING
import logging
from datetime import timedelta
import time
import warnings
import pathlib

import numpy as np
from numpy.polynomial import Polynomial
import networkx as nx
from scipy import interpolate, sparse, optimize
import xarray as xr
from traits.api import HasStrictTraits
import pandas as pd

from oopnet.utils import utils
from oopnet.report.report import SimulationReport
from oopnet.utils.oopnet_logging import logging_decorator

if TYPE_CHECKING:
    from oopnet.elements.network import Network

from ..utils.getters.vectors import v_demand, v_demandpattern, v_roughness, v_length, v_tankdiameter, \
    v_elevation
from ..utils.getters.element_lists import get_node_ids, get_pipe_ids, get_junctions, get_tanks, get_reservoirs, \
    get_junction_ids, get_pipes
from ..utils.getters.get_by_id import get_pattern
from ..graph.graph import onlinks2nxlinks, MultiDiGraph

from ..hydraulics.pipes import compute_cross_sectional_areas as compute_pipe_cross_sectional_areas
from ..hydraulics.tanks import compute_cross_sectional_areas as compute_tank_cross_sectional_areas
from ..hydraulics.demands import compute_interpolators_of_the_demands_at_junctions, \
    interpolate_demands_from_interpolators
from ..hydraulics.friction_headlosses import compute_friction_coefficients, \
    compute_regularized_friction_headlosses_until_x, compute_friction_headlosses_per_1000m, \
    compute_cubic_polynomial_approximation_residuals_for_flows_close_to_zero
from ..hydraulics.velocities import compute_velocities
from ..hydraulics.heads import compute_heads_from_pressure_heads, compute_pressure_heads_from_heads
from ..hydraulics.consumptions import MINIMUM_PRESSURE_HEAD_AT_JUNCTIONS, SERVICE_PRESSURE_HEAD_AT_JUNCTIONS, \
    compute_cubic_polynomial_approximation_residuals_for_pressure_fractions_close_to_zero, \
    compute_cubic_polynomial_approximation_residuals_for_pressure_fractions_close_to_one, compute_pressure_fractions, \
    compute_consumptions, compute_regularized_unitary_consumptions, compute_pressure_fraction_derivative

from ..elements.system_operation import Pattern

from ..solvers import compute_headlosses_from_source_nodes, compute_energy_residuals_in_pipes, \
    compute_mass_residuals_at_junctions
from ..solvers.newton import solve_balance_equations, compute_jacobian_schur_complement_matrix_condition_number
from ..solvers.ode import compute_approx_new_heads_at_tanks_with_forward_euler_method, \
    compute_new_heads_at_tanks_with_trapezoidal_rule_method

from ..elements.component_registry import ComponentNotExistingError

logger = logging.getLogger(__name__)


@logging_decorator(logger)
class ModelSimulator:
    """Runs a simulation by calling the Python simulator

    Attributes:
      thing: either an OOPNET network object or the filename of an EPANET input file
      filename: if thing is an OOPNET network, filename is an option to perform command line EPANET simulations with a specific filename. If filename is a Python None object then a file with a random UUID (universally unique identifier) is generated
      delete: if delete is True the EPANET Input and Report file is deleted, if False then the simulation results won't be deleted and are stored in a folder named path
      path: Path were to perform the simulations. If path is a Python None object then a tmp-folder is generated

    Returns:
      OOPNET report object

    """

    def __init__(
        self,
        thing: Union[Network, str],
        filename: Optional[str] = None,
        delete: bool = True,
        path: Optional[str] = None,
        startdatetime: Optional[datetime.datetime] = None,
        output: bool = False,
    ):
        self.thing = thing
        self.filename = filename
        self.delete = delete
        self.path = path
        self.startdatetime = startdatetime
        self.output = output

    def _set_path(self):
        """Sets path for temporary file placement."""
        # Set Path and generate it, if it does not exist
        if self.path is None:
            self.path = "tmp"
            utils.mkdir(self.path)
        elif isinstance(self.path, str):
            if not os.path.isdir(self.path):
                utils.mkdir(self.path)
        else:
            raise TypeError(
                f"Path must either be None or of type string but a value of type {type(self.path)} was"
                f"submitted"
            )

    def _set_filename(self):
        """Sets filename for temporary file placement."""
        if isinstance(self.thing, str):
            self.filename = os.path.join(self.path, os.path.split(self.thing)[-1])
            shutil.copy(self.thing, self.filename)
        else:
            self.filename = os.path.join(
                self.path, str(uuid.uuid4()) + ".inp"
            )  # generate filename with unique filename

    def _setup_report(self):
        """Sets up report."""
        if self.thing.report.nodes == "NONE" or not self.thing.report.nodes:
            self.thing.report.nodes = "ALL"
        if self.thing.report.links == "NONE" or not self.thing.report.links:
            self.thing.report.links = "ALL"

    def run(self):

        """Simulates a hydraulic model using the Python simulator."""
        logging.info("Simulating model")

        self._setup_report()

        if not self.delete:
            self._set_path()
            self._set_filename()
            self.thing.write(filename=self.filename)

        res = Run(self.thing, startdatetime=self.startdatetime, return_run_info=self.output)

        if self.output:
            rpt, rinf = res
            if not self.delete:
                outputs_dirpath = os.path.join(self.path, 'Outputs')
                write_report_to_csv(rpt, dirpath=outputs_dirpath, float_format=None)
                write_run_info_to_csv(rinf, dirpath=outputs_dirpath)
                logger.info('Outputs are in directory {}'.format(outputs_dirpath))
                print('Outputs are in directory {}'.format(outputs_dirpath))
        else:
            rpt = res

        rpt = SimulationReport(
            report=rpt,
        )

        if rpt:
            return rpt


class EPSException(Exception):
    """Custom exception to raise when an error occurs."""
    pass


class EPSWarning(Warning):
    """Custom class to issue a warning."""
    pass


class Run(HasStrictTraits):
    """Class to run an EPS with PDM consumptions."""

    ABSOLUTE_TOLERANCE_ON_HYDRAULIC_OUTPUTS_RESIDUALS = 1e-2
    """Absolute tolerance on residuals obtained at the end of Newton's algorithm, under which we consider the hydraulic  
    solution found is accurate enough"""

    ABSOLUTE_TOLERANCE_ON_REPORTING_OUTPUTS_RESIDUALS = 1e-2
    """Absolute tolerance on the residuals of reporting outputs (obtained after possible interpolation of hydraulic 
    outputs), under which we consider the hydraulic solution found is accurate enough"""

    def __new__(cls, network, startdatetime, return_run_info):
        """
        Convert OOPNet `network` to matrix structure, compute initial conditions, run the simulation over the time grid,
        and return its results.

        :param network: OOPNet network object to simulate
        :return: simulation outputs, consisting of an OOPNet report (i.e. two xarray.DataArray of parameters and
        variables: one for nodes and one for links), and, if the user asked for returning run info too, then also return a
        dictionary of metrics and error log, which keys are: 'hydraulic_metrics', 'reporting_metrics', 'constant_metrics',
        'hydraulic_errors' and 'reporting_errors', each of them corresponding to an xarray.DataArray with appropriate
        coordinates and data types.
        """

        # 1. retrieve process time for profiling

        cls.process_start_time = time.process_time()  # sum of the kernel and user-space CPU time

        # 2. get parameters from OOPNet `network` object

        # junctions
        junctions = get_junctions(network)
        cls.junction_ids = get_junction_ids(network)
        cls.number_of_junctions = len(junctions)
        cls.junction_elevations = np.array([junction.elevation for junction in junctions])
        default_demand_pattern = network.options.pattern
        try:
            default_demand_pattern = get_pattern(network, default_demand_pattern)
        except ComponentNotExistingError:
            # pattern '1' not found ; set default demand pattern to constant pattern
            default_demand_pattern = Pattern(id='1')
            default_demand_pattern.multipliers = [1.0]
        demand_patterns = v_demandpattern(network)
        global_demand_multiplier = network.options.demandmultiplier
        if global_demand_multiplier is None:
            global_demand_multiplier = 1.0
        nominal_demands = v_demand(network)

        # reservoirs
        reservoirs = get_reservoirs(network)
        cls.number_of_reservoirs = len(reservoirs)
        if cls.number_of_reservoirs == 0:
            cls.with_reservoir = False
            cls.heads_at_reservoirs = None
            cls.max_head_at_reservoirs = None
        else:
            cls.heads_at_reservoirs = np.array([reservoir.head for reservoir in reservoirs])
            cls.max_head_at_reservoirs = cls.heads_at_reservoirs.max()
            cls.with_reservoir = True

        # tanks
        tanks = get_tanks(network)
        number_of_tanks = len(tanks)
        cls.tank_elevations = None
        tank_initial_levels = None
        tank_diameters = None
        if number_of_tanks == 0:
            cls.with_tank = False
        else:
            cls.with_tank = True
            cls.tank_elevations = np.array([tank.elevation for tank in tanks])
            tank_initial_levels = np.array([tank.initlevel for tank in tanks])
            tank_diameters = v_tankdiameter(network)

        # all nodes
        cls.node_ids = get_node_ids(network)
        cls.node_elevations = v_elevation(network)

        # all nodes except reservoirs
        cls.number_of_junctions_and_tanks = cls.number_of_junctions + number_of_tanks

        # pipes
        cls.pipe_ids = get_pipe_ids(network)
        cls.pipe_diameters = np.asarray([x.diameter for x in get_pipes(network)])
        cls.pipe_lengths = v_length(network)
        cls.number_of_pipes = len(cls.pipe_ids)
        cls.pipe_cross_sectional_areas = compute_pipe_cross_sectional_areas(cls.pipe_diameters)
        pipe_roughnesses = v_roughness(network)

        # simulation times
        start_time = network.times.startclocktime
        if start_time is None:
            cls.start_clock_time_in_seconds = 0.0
        else:
            cls.start_clock_time_in_seconds = start_time.total_seconds()
        duration = network.times.duration
        if duration is None:
            cls.duration_in_seconds = 0.0
        else:
            cls.duration_in_seconds = duration.total_seconds()
        pattern_time_step = network.times.patterntimestep
        if pattern_time_step is None:
            pattern_time_step_in_seconds = 3600.0
        else:
            pattern_time_step_in_seconds = pattern_time_step.total_seconds()
        pattern_start_time = network.times.patternstart
        if pattern_start_time is None:
            pattern_start_in_seconds = 0.0
        else:
            pattern_start_in_seconds = pattern_start_time.total_seconds()
        if cls.duration_in_seconds == 0.0:
            cls.is_single_period_snapshot_analysis = True
        else:
            cls.is_single_period_snapshot_analysis = False
            hydraulic_time_step = network.times.hydraulictimestep
            if hydraulic_time_step is None:
                cls.hydraulic_time_step_in_seconds = 0.0
            else:
                cls.hydraulic_time_step_in_seconds = hydraulic_time_step.total_seconds()
            reporting_time_step = network.times.reporttimestep
            if reporting_time_step is None:
                cls.reporting_time_step_in_seconds = 0.0
            else:
                cls.reporting_time_step_in_seconds = reporting_time_step.total_seconds()
            cls.hydraulic_time_step_in_seconds = min(
                cls.hydraulic_time_step_in_seconds, cls.reporting_time_step_in_seconds, pattern_time_step_in_seconds)
        report_start_time = network.times.reportstart
        if report_start_time is None:
            cls.reporting_start_time_in_seconds = 0.0
        else:
            cls.reporting_start_time_in_seconds = report_start_time.total_seconds()
        cls.startdatetime = startdatetime

        # incidence matrices
        graph_of_the_network = MultiDiGraph(network, weight='')
        network_edges = onlinks2nxlinks(network)
        number_of_edges = len(network_edges)
        if number_of_edges > cls.number_of_pipes:
            warnings.warn('The network contains at least one link which is not a pipe (e.g., pump, valve, etc.). Links other than pipes are ignored in current version of the simulator.', EPSWarning)
            network_edges = network_edges[:cls.number_of_pipes]
        cls.incidence_matrix = - nx.incidence_matrix(
            graph_of_the_network, nodelist=cls.node_ids, edgelist=network_edges, oriented=True)
        cls.incidence_matrix_reduced_to_junctions = cls.incidence_matrix[:cls.number_of_junctions, :]
        if cls.with_tank:
            cls.incidence_matrix_reduced_to_tanks = \
                cls.incidence_matrix[cls.number_of_junctions:cls.number_of_junctions_and_tanks, :]
        else:
            cls.incidence_matrix_reduced_to_tanks = None
        if cls.with_reservoir:
            cls.incidence_matrix_reduced_to_reservoirs = cls.incidence_matrix[cls.number_of_junctions_and_tanks:, :]
        else:
            cls.incidence_matrix_reduced_to_reservoirs = None

        # run info
        cls.return_run_info = return_run_info  # flag for returning (or not) run info (i.e. run metrics
        # and error/warning messages) ; note: run info will be computed anyway

        # 3. compute derived parameters

        cls.demands_at_junctions_interpolators = \
            compute_interpolators_of_the_demands_at_junctions(
                nominal_demands, global_demand_multiplier, demand_patterns, default_demand_pattern,
                pattern_time_step_in_seconds, pattern_start_in_seconds, cls.duration_in_seconds)

        if cls.with_tank:
            # parameters needed to update heads at tanks
            tank_cross_sectional_areas = compute_tank_cross_sectional_areas(tank_diameters)
            inverses_of_tank_cross_sectional_areas = 1 / tank_cross_sectional_areas
            cls.tanks_inertia_inverse_matrix = sparse.diags(inverses_of_tank_cross_sectional_areas)

        # regularization of friction headlosses
        cls.friction_coefficients = compute_friction_coefficients(cls.pipe_diameters, pipe_roughnesses)
        a1, a3 = optimize.root(
            compute_cubic_polynomial_approximation_residuals_for_flows_close_to_zero, np.zeros(2, dtype=float)).x
        cls.reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero = Polynomial([0, a1, 0, a3])
        cls.reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero \
            = cls.reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero.deriv()

        # regularization of consumptions at junctions
        cls.unitary_consumption_regularization_close_to_zero = Polynomial(optimize.root(
            compute_cubic_polynomial_approximation_residuals_for_pressure_fractions_close_to_zero,
            np.zeros(4, dtype=float)).x)
        cls.unitary_consumption_regularization_close_to_one = Polynomial(optimize.root(
            compute_cubic_polynomial_approximation_residuals_for_pressure_fractions_close_to_one,
            np.zeros(4, dtype=float)).x)
        cls.unitary_consumption_derivative_regularization_close_to_zero \
            = cls.unitary_consumption_regularization_close_to_zero.deriv()
        cls.unitary_consumption_derivative_regularization_close_to_one \
            = cls.unitary_consumption_regularization_close_to_one.deriv()
        # pressure fraction derivative
        cls.pressure_fraction_derivative = compute_pressure_fraction_derivative()

        cls.fixed_parameters_needed_by_solver \
            = {'number_of_pipes': cls.number_of_pipes, 'heads_at_reservoirs': cls.heads_at_reservoirs,
               'incidence_matrix_reduced_to_tanks': cls.incidence_matrix_reduced_to_tanks,
               'incidence_matrix_reduced_to_reservoirs': cls.incidence_matrix_reduced_to_reservoirs,
               'number_of_junctions': cls.number_of_junctions, 'max_head_at_reservoirs': cls.max_head_at_reservoirs,
               'junction_elevations': cls.junction_elevations,
               'unitary_consumption_regularization_close_to_zero': cls.unitary_consumption_regularization_close_to_zero,
               'unitary_consumption_regularization_close_to_one': cls.unitary_consumption_regularization_close_to_one,
               'friction_coefficients': cls.friction_coefficients, 'pipe_lengths': cls.pipe_lengths,
               'reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero':
                   cls.reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero,
               'incidence_matrix_reduced_to_junctions': cls.incidence_matrix_reduced_to_junctions,
               'unitary_consumption_derivative_regularization_close_to_zero':
                   cls.unitary_consumption_derivative_regularization_close_to_zero,
               'unitary_consumption_derivative_regularization_close_to_one':
                   cls.unitary_consumption_derivative_regularization_close_to_one,
               'pressure_fraction_derivative': cls.pressure_fraction_derivative,
               'reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero':
                   cls.reduced_unitary_friction_headloss_derivative_regularization_for_flows_close_to_zero}

        # 4. set initial conditions

        cls.demands_at_junctions_at_start_time = \
            interpolate_demands_from_interpolators(
                cls.start_clock_time_in_seconds, cls.demands_at_junctions_interpolators)

        if cls.with_tank:
            # heads at tanks
            cls.heads_at_tanks_at_start_time = compute_heads_from_pressure_heads(
                tank_initial_levels, cls.tank_elevations)

        cls.flows_at_start_time = np.full(cls.number_of_pipes, 0.5, dtype=float)

        cls.heads_at_junctions_at_start_time = \
            MINIMUM_PRESSURE_HEAD_AT_JUNCTIONS + cls.junction_elevations \
            + (SERVICE_PRESSURE_HEAD_AT_JUNCTIONS - MINIMUM_PRESSURE_HEAD_AT_JUNCTIONS) / 5 + 0.5

        # 6. set other python parameters

        # following flag will become (and remain) False as soon as the algorithm fails to converge at any hydraulic time
        # step
        cls.never_failed = True

        # create lists to store all the error messages along the simulation
        cls.hydraulic_errors = []
        cls.reporting_errors = []

        # 7. run the simulation and return its results
        return cls._run()

    @classmethod
    def _run(cls):
        """Simulate the system over the time grid, then create an OOPNET report object and report it.
        If the user asked for returning run info, then also return metrics and error/warning messages"""

        # construct the time grid
        if cls.is_single_period_snapshot_analysis or cls.hydraulic_time_step_in_seconds == 0:
            cls.length_of_hydraulic_time_grid = 1
            hydraulic_time_grid_in_seconds = np.array([cls.start_clock_time_in_seconds])
        else:
            cls.length_of_hydraulic_time_grid = \
                int(cls.duration_in_seconds / cls.hydraulic_time_step_in_seconds) + 1
            hydraulic_time_grid_in_seconds = np.linspace(
                cls.start_clock_time_in_seconds, cls.start_clock_time_in_seconds + cls.duration_in_seconds,
                cls.length_of_hydraulic_time_grid)

        # create lists to store flows, heads at junctions, time deltas and tun info over hydraulic time grid
        flows_over_hydraulic_time_grid = []
        heads_at_junctions_over_hydraulic_time_grid = []
        heads_at_tanks_over_hydraulic_time_grid = None
        if cls.with_tank:
            previous_heads_at_tanks = cls.heads_at_tanks_at_start_time
            heads_at_tanks_over_hydraulic_time_grid = [previous_heads_at_tanks]
        else:
            previous_heads_at_tanks = None
        hydraulic_time_grid_in_time_deltas = []
        run_info_over_hydraulic_time_grid = []

        demands_at_junctions = cls.demands_at_junctions_at_start_time

        previous_flows = cls.flows_at_start_time
        previous_heads_at_junctions = cls.heads_at_junctions_at_start_time

        previous_flows_m3 = None  # define it here just to avoid a "Local variable ... might be referenced before
        # assignment" warning

        # start the simulation loop
        for current_time_step, current_time_in_seconds in enumerate(hydraulic_time_grid_in_seconds, start=1):

            current_timedelta = timedelta(seconds=current_time_in_seconds)
            hydraulic_time_grid_in_time_deltas.append(current_timedelta)

            # init the error sub-list associated to current hydraulic time step
            cls.hydraulic_errors.append([])

            # solve balance equation
            new_flows, new_heads_at_junctions, solver_metrics = cls._solve_balance_equation_at_current_time_step(
                current_time_step, current_timedelta, previous_flows, previous_heads_at_junctions, demands_at_junctions,
                previous_heads_at_tanks)

            flows_over_hydraulic_time_grid.append(new_flows)
            heads_at_junctions_over_hydraulic_time_grid.append(new_heads_at_junctions)

            # flatten the metrics
            (status, number_of_iterations, number_of_damping_corrections, order_of_convergence,
             process_time) = (solver_metrics[key] for key
                              in ['status', 'number_of_iterations', 'number_of_damping_corrections',
                                  'order_of_convergence', 'process_time'])
            res_norms = solver_metrics['residual_norms']
            (res_norm_1, res_norm_2, res_norm_inf) = (res_norms[key] for key in [1, 2, np.inf])
            flattened_metrics = [status, number_of_iterations, number_of_damping_corrections, res_norm_1, res_norm_2,
                                 res_norm_inf, order_of_convergence, process_time]
            run_info_over_hydraulic_time_grid.append(flattened_metrics)

            if current_time_in_seconds < hydraulic_time_grid_in_seconds[-1]:
                # update variables for next iteration
                if cls.with_tank:
                    # update heads at tanks
                    new_flows_m3 = new_flows / 1000
                    if current_time_step == 1:
                        # first time step: apply Heun's method for a better estimate of new heads at tanks
                        new_flows, new_flows_m3, new_heads_at_junctions, new_heads_at_tanks = \
                            cls._compute_new_heads_at_tanks_with_heun_method(
                                current_time_step, current_timedelta, previous_heads_at_tanks, new_flows, new_flows_m3,
                                new_heads_at_junctions, demands_at_junctions)
                    else:
                        # this is not the first time step: apply trapezoidal rule method directly
                        new_heads_at_tanks = compute_new_heads_at_tanks_with_trapezoidal_rule_method(
                            cls.hydraulic_time_step_in_seconds, previous_heads_at_tanks, previous_flows_m3,
                            new_flows_m3, cls.incidence_matrix_reduced_to_tanks, cls.tanks_inertia_inverse_matrix)
                    # store new heads at tanks ...
                    heads_at_tanks_over_hydraulic_time_grid.append(new_heads_at_tanks)
                    # ... and reset previous heads at_tanks and previous flows in m3/s for next iteration
                    previous_heads_at_tanks = new_heads_at_tanks
                    previous_flows_m3 = new_flows_m3
                # update flows, heads at junctions, and demands for next iteration
                previous_flows = new_flows
                previous_heads_at_junctions = new_heads_at_junctions
                demands_at_junctions = interpolate_demands_from_interpolators(
                    current_time_in_seconds + cls.hydraulic_time_step_in_seconds,
                    cls.demands_at_junctions_interpolators)
                # and continue to next iteration

        # integration over the hydraulic time grid ended ; we now have flows, heads at junctions and heads at
        # tanks over the full hydraulic time grid

        # let's now compute flows, heads at junctions and heads at tanks over the reporting time grid ; reporting time
        # grid may differ from the hydraulic one because report start time can be non-zero and/or report time step can
        # differ from hydraulic time step
        reporting_duration_in_seconds = cls.duration_in_seconds - cls.reporting_start_time_in_seconds
        reporting_duration_in_seconds = max(0, reporting_duration_in_seconds)
        heads_at_tanks_over_reporting_time_grid = None
        if cls.is_single_period_snapshot_analysis:
            # in this case this is simple: reporting variables are exactly the same as the hydraulic ones
            reporting_time_grid_in_seconds = np.array([cls.reporting_start_time_in_seconds])
            flows_over_reporting_time_grid = np.array(flows_over_hydraulic_time_grid)
            heads_at_junctions_over_reporting_time_grid = np.array(heads_at_junctions_over_hydraulic_time_grid)
            if cls.with_tank:
                heads_at_tanks_over_reporting_time_grid = np.array(heads_at_tanks_over_hydraulic_time_grid)
            length_of_reporting_time_grid = 1
        else:
            # otherwise, first construct the reporting time grid ...
            reporting_time_grid_in_seconds = \
                np.linspace(cls.reporting_start_time_in_seconds,
                            cls.reporting_start_time_in_seconds + reporting_duration_in_seconds,
                            int(reporting_duration_in_seconds / cls.reporting_time_step_in_seconds) + 1)
            length_of_reporting_time_grid = len(reporting_time_grid_in_seconds)
            # ... and test if reporting and hydraulic time_steps are the same or not
            if cls.reporting_time_step_in_seconds == cls.hydraulic_time_step_in_seconds:
                # they are the same ; then just extract the variables at the time step(s) we need (not need for
                # interpolation)
                number_of_unreported_time_steps = cls.length_of_hydraulic_time_grid - length_of_reporting_time_grid
                flows_over_reporting_time_grid = \
                    np.array(flows_over_hydraulic_time_grid[number_of_unreported_time_steps:])
                heads_at_junctions_over_reporting_time_grid = np.array(
                    heads_at_junctions_over_hydraulic_time_grid[number_of_unreported_time_steps:])
                if cls.with_tank:
                    heads_at_tanks_over_reporting_time_grid = np.array(
                        heads_at_tanks_over_hydraulic_time_grid[number_of_unreported_time_steps:])
            else:
                # otherwise we need, to construct the reporting outputs, to interpolate the variables computed on the
                # hydraulic time grid
                flows_over_reporting_time_grid = []
                heads_at_junctions_over_reporting_time_grid = []
                if cls.with_tank:
                    heads_at_tanks_over_reporting_time_grid = []
                variables_over_hydraulic_and_reporting_time_grids = [
                    (flows_over_hydraulic_time_grid, flows_over_reporting_time_grid),
                    (heads_at_junctions_over_hydraulic_time_grid, heads_at_junctions_over_reporting_time_grid)]
                if cls.with_tank:
                    variables_over_hydraulic_and_reporting_time_grids += [
                        (heads_at_tanks_over_hydraulic_time_grid, heads_at_tanks_over_reporting_time_grid)]
                for variables_over_hydraulic_time_grid, variables_over_reporting_time_grid \
                        in variables_over_hydraulic_and_reporting_time_grids:
                    for variable_over_hydraulic_time_grid in np.array(variables_over_hydraulic_time_grid).T:
                        # we use PCHIP 1-D monotonic cubic interpolation from SciPy ; this prevent variables from
                        # becoming negative when should not
                        variable_interpolator = interpolate.PchipInterpolator(
                            hydraulic_time_grid_in_seconds, variable_over_hydraulic_time_grid)
                        variable_over_reporting_time_grid = variable_interpolator(
                            reporting_time_grid_in_seconds)
                        variables_over_reporting_time_grid.append(variable_over_reporting_time_grid)
                flows_over_reporting_time_grid = np.array(flows_over_reporting_time_grid).T
                heads_at_junctions_over_reporting_time_grid = np.array(heads_at_junctions_over_reporting_time_grid).T
                if cls.with_tank:
                    heads_at_tanks_over_reporting_time_grid = np.array(heads_at_tanks_over_reporting_time_grid).T

        # now that we have all the (potentially interpolated) reporting variables, let's construct the full reporting
        # outputs, and the run info (if asked by the user)

        reporting_time_grid_in_time_deltas = []
        nodes_reports_over_reporting_time_grid_list = []
        pipes_reports_over_reporting_time_grid_list = []
        run_info_over_reporting_time_grid = []

        # loop over the reporting time grid
        for i in range(length_of_reporting_time_grid):

            # init the error sub-list associated to current reporting time step
            cls.reporting_errors.append([])

            # retrieve the values of the variables over the reporting time grid
            current_time_in_seconds = reporting_time_grid_in_seconds[i]
            flows = flows_over_reporting_time_grid[i]
            heads_at_junctions = heads_at_junctions_over_reporting_time_grid[i]
            if cls.with_tank:
                heads_at_tanks = heads_at_tanks_over_reporting_time_grid[i]
            else:
                heads_at_tanks = None

            current_timedelta = timedelta(seconds=current_time_in_seconds)
            if cls.startdatetime is not None:
                current_timedelta += cls.startdatetime

            reporting_time_grid_in_time_deltas.append(current_timedelta)

            # compute the derived variables to report

            # heads
            to_concat = [heads_at_junctions]
            if cls.with_tank:
                # ATTENTION: for nodes, the concatenation must be done in the same order as `cls.node_ids`, i.e.:
                # junctions, tanks and reservoirs
                to_concat.append(heads_at_tanks)
            if cls.with_reservoir:
                to_concat.append(cls.heads_at_reservoirs)
            heads = np.concatenate(to_concat)

            # pressures
            pressures = compute_pressure_heads_from_heads(heads, cls.node_elevations)
            if cls.with_reservoir:
                pressures[-cls.number_of_reservoirs:] = 0

            demands_at_junctions = interpolate_demands_from_interpolators(
                current_time_in_seconds, cls.demands_at_junctions_interpolators)

            # consumptions
            pressure_fractions = compute_pressure_fractions(heads_at_junctions, cls.junction_elevations)
            unitary_consumptions = compute_regularized_unitary_consumptions(
                pressure_fractions, cls.unitary_consumption_regularization_close_to_zero,
                cls.unitary_consumption_regularization_close_to_one)
            consumptions_at_junctions = compute_consumptions(unitary_consumptions, demands_at_junctions)
            negative_consumptions_at_junctions_mask = consumptions_at_junctions < 0
            # negative_consumptions_at_junctions_mask might be non-empty if the variables over reporting time grid come
            # from interpolation ; but then, the negative consumptions should be very close to zero ; let's check it
            negative_consumptions_at_junctions = consumptions_at_junctions[negative_consumptions_at_junctions_mask]
            if not np.allclose(negative_consumptions_at_junctions, 0,
                               atol=cls.ABSOLUTE_TOLERANCE_ON_REPORTING_OUTPUTS_RESIDUALS):
                minimum_consumption = negative_consumptions_at_junctions.min()
                warnings.warn(
                    'At least one of the computed consumptions is negative (minimum is {} l/s). Force them to 0.'
                    .format(minimum_consumption), EPSWarning)
            # then, threshold negative consumptions to 0
            consumptions_at_junctions[negative_consumptions_at_junctions_mask] = 0
            consumptions = np.empty_like(heads)
            consumptions[:cls.number_of_junctions] = consumptions_at_junctions
            consumptions[cls.number_of_junctions:] = 0

            # unitary consumptions at junctions (%) ; unitary consumptions are equal to 100 % where
            # demands are equal (or almost equal) to 0 or to consumptions, and equal to the quotient of consumptions
            # over demands multiplied by 100 elsewhere
            unitary_consumptions_at_junctions = np.empty_like(demands_at_junctions)
            fully_satisfied_demands_mask = \
                np.isclose(demands_at_junctions, 0) | np.isclose(consumptions_at_junctions, demands_at_junctions)
            unitary_consumptions_at_junctions[fully_satisfied_demands_mask] = 100
            not_fully_satisfied_demands_mask = ~fully_satisfied_demands_mask
            unitary_consumptions_at_junctions[not_fully_satisfied_demands_mask] = \
                consumptions_at_junctions[not_fully_satisfied_demands_mask] \
                / demands_at_junctions[not_fully_satisfied_demands_mask] * 100
            unitary_consumptions = np.empty_like(heads)
            unitary_consumptions[:cls.number_of_junctions] = unitary_consumptions_at_junctions
            unitary_consumptions[cls.number_of_junctions:] = np.nan

            # outflows at nodes
            outflows = - cls.incidence_matrix @ flows

            # demands
            demands = np.empty_like(heads)
            demands[:cls.number_of_junctions] = demands_at_junctions
            demands[cls.number_of_junctions:] = outflows[cls.number_of_junctions:]

            # friction head losses
            friction_headlosses = compute_regularized_friction_headlosses_until_x(
                flows, cls.friction_coefficients, cls.pipe_lengths,
                cls.reduced_unitary_friction_headloss_regularization_for_flows_close_to_zero)
            headlosses_per_1000m = compute_friction_headlosses_per_1000m(friction_headlosses, cls.pipe_lengths)
            headlosses_per_1000m_abs = np.abs(headlosses_per_1000m)

            # velocities
            velocities = compute_velocities(flows, cls.pipe_cross_sectional_areas)

            # energy and mass residuals (for last check and for the run info to return)
            headlosses_from_source_nodes = compute_headlosses_from_source_nodes(
                cls.number_of_pipes, heads_at_tanks, cls.heads_at_reservoirs, cls.incidence_matrix_reduced_to_tanks,
                cls.incidence_matrix_reduced_to_reservoirs)
            energy_residuals = compute_energy_residuals_in_pipes(
                friction_headlosses, heads_at_junctions, headlosses_from_source_nodes,
                cls.incidence_matrix_reduced_to_junctions)
            outflows_at_junctions = outflows[:cls.number_of_junctions]
            mass_residuals = compute_mass_residuals_at_junctions(
                flows, outflows_at_junctions, cls.incidence_matrix_reduced_to_junctions)
            all_residuals = np.concatenate([energy_residuals, mass_residuals])
            # check that residuals from outputs to report are low enough
            inf_norm_of_residuals = np.linalg.norm(all_residuals, ord=np.inf)
            res_norms = None
            if inf_norm_of_residuals > cls.ABSOLUTE_TOLERANCE_ON_REPORTING_OUTPUTS_RESIDUALS:
                res_norms = {}
                for ord_ in (1, 2):
                    res_norms[ord_] = np.linalg.norm(all_residuals, ord=ord_)
                error_message = \
                    'Inf. norm on residuals from outputs to report ({}) greater than permitted absolute tolerance ' \
                    '({}). Other computed norms are: {}.'.format(
                        inf_norm_of_residuals, cls.ABSOLUTE_TOLERANCE_ON_REPORTING_OUTPUTS_RESIDUALS, res_norms)
                warnings.warn(error_message, EPSWarning)
                cls.reporting_errors[-1].append(error_message)
                cls.never_failed = False

            # construct OOPNet report for current reporting time step

            nodes_report = xr.DataArray(data=np.vstack([cls.node_elevations, demands, heads, pressures, consumptions, unitary_consumptions]).T,
                                        coords={'time': current_timedelta, 'id': cls.node_ids,
                                                'vars': ['Elevation', 'Demand', 'Head', 'Pressure', 'Consumption', 'UnitaryConsumption']},
                                        dims=('id', 'vars'))

            nodes_reports_over_reporting_time_grid_list.append(nodes_report)

            pipes_report = xr.DataArray(data=np.vstack((cls.pipe_lengths, cls.pipe_diameters, flows, velocities,
                                                        headlosses_per_1000m_abs, headlosses_per_1000m,
                                                        cls.friction_coefficients)).T,
                                        coords={'time': current_timedelta, 'id': cls.pipe_ids,
                                                'vars': ['Length', 'Diameter', 'Flow', 'Velocity', 'Headloss',
                                                         'Headloss Signed', 'Friction Factor']},
                                        dims=('id', 'vars'))

            pipes_reports_over_reporting_time_grid_list.append(pipes_report)

            # and run info
            if res_norms is None:
                res_norms = {}
                for ord_ in (1, 2):
                    res_norms[ord_] = np.linalg.norm(all_residuals, ord=ord_)
            run_info_over_reporting_time_grid.append(
                [res_norms[1], res_norms[2], inf_norm_of_residuals])

        # then concat all sub-reports of the reporting time grid ...
        if length_of_reporting_time_grid > 1:
            nodes_report_xarray = xr.concat(nodes_reports_over_reporting_time_grid_list, dim='time')
            pipes_report_xarray = xr.concat(pipes_reports_over_reporting_time_grid_list, dim='time')
        else:
            nodes_report_xarray = nodes_reports_over_reporting_time_grid_list[-1].drop_vars('time')
            pipes_report_xarray = pipes_reports_over_reporting_time_grid_list[-1].drop_vars('time')
        for component_type_name, report_xarray in (('Node', nodes_report_xarray), ('pipe', pipes_report_xarray)):
            report_xarray.name = '{}Report'.format(component_type_name)
        # ... and create the full OOPNet report (i.e. the report over the full reporting time grid)
        oopnet_report = (nodes_report_xarray, pipes_report_xarray)
        to_return = oopnet_report

        if cls.return_run_info:
            # concatenate run info over the full hydraulic time grid
            # metrics
            hydraulic_metrics = xr.DataArray(
                data=run_info_over_hydraulic_time_grid,
                coords={'time': hydraulic_time_grid_in_time_deltas,
                        'vars': ['status', 'number_of_iterations', 'number_of_damping_corrections', 'residuals_1_norm',
                                 'residuals_2_norm', 'residuals_inf_norm', 'order_of_convergence', 'process_time']},
                dims=('time', 'vars'), name='HydraulicMetrics')
            # errors
            hydraulic_errors = Run._concatenate_error_messages_per_time_step(cls.hydraulic_errors)
            hydraulic_errors = xr.DataArray(
                data=hydraulic_errors,
                coords={'time': hydraulic_time_grid_in_time_deltas, 'vars': ['errors']},
                dims=('time', 'vars'), name='HydraulicErrors')
            # concatenate run info over the full reporting time grid
            # metrics
            reporting_metrics = xr.DataArray(
                data=run_info_over_reporting_time_grid,
                coords={'time': reporting_time_grid_in_time_deltas,
                        'vars': ['residuals_1_norm', 'residuals_2_norm', 'residuals_inf_norm']},
                dims=('time', 'vars'), name='ReportingMetrics')
            # errors
            reporting_errors = Run._concatenate_error_messages_per_time_step(cls.reporting_errors)
            reporting_errors = xr.DataArray(
                data=reporting_errors,
                coords={'time': reporting_time_grid_in_time_deltas, 'vars': ['errors']},
                dims=('time', 'vars'), name='ReportingErrors')
            # time independent metrics
            total_process_time = time.process_time() - cls.process_start_time
            constant_metrics = xr.DataArray(
                data=[cls.never_failed, total_process_time], coords={'vars': ['success', 'total_process_time']},
                dims=('vars',), name='ConstantMetrics')

            all_run_info = {'hydraulic_metrics': hydraulic_metrics, 'reporting_metrics': reporting_metrics,
                            'constant_metrics': constant_metrics, 'hydraulic_errors': hydraulic_errors,
                            'reporting_errors': reporting_errors}

            to_return = (to_return, all_run_info)

        return to_return

    @classmethod
    def _solve_balance_equation_at_current_time_step(
            cls, current_time_step, current_timedelta, previous_flows, previous_heads_at_junctions,
            demands_at_junctions, heads_at_tanks):
        """
        Protect the call to solver into a try-except clause. If no exception is raised, then compute derived
        metrics, and return new flows, new heads at junctions, and new computed metrics.

        :param current_time_step: current time step (ordinal number)
        :param current_timedelta: current time delta (of type `datetime.timedelta`)
        :param previous_flows: flows at previous time step
        :param previous_heads_at_junctions: heads at junctions at previous time step
        :param demands_at_junctions: demands at current time step
        :param heads_at_tanks: heads at tanks at current time step
        :return: new flows, new heads at junctions, and computed metrics.
        """
        start_time = time.process_time()  # for metrics

        try:
            (new_flows, new_heads_at_junctions, status, raw_metrics, error_messages) = solve_balance_equations(
                previous_flows, previous_heads_at_junctions, demands_at_junctions, heads_at_tanks,
                cls.fixed_parameters_needed_by_solver)
        except EPSException as e:
            # solver did not converge ; then set
            cls.never_failed = False
            # convert exception to string
            e_str = str(e)
            # amend last list of hydraulic errors
            cls.hydraulic_errors[-1].append(e_str)
            # and re-raised an exception
            raise EPSException('At time step = {} / {} (i.e. clock time = {}): {}'.format(
                current_time_step, cls.length_of_hydraulic_time_grid, current_timedelta, e_str))

        # solver ended ; then, first retrieve returned raw metrics ...
        (residuals, number_of_iterations, res_diffs_per_iteration, number_of_damping_corrections) = \
            (raw_metrics[key] for key in
             ['residuals', 'number_of_iterations', 'res_diffs_per_iteration', 'number_of_damping_corrections'])
        # ... then check residuals against cls.ABSOLUTE_TOLERANCE_ON_HYDRAULIC_OUTPUTS_RESIDUALS ...
        res_inf_norm = np.linalg.norm(residuals, ord=np.inf)
        res_norms = None
        if res_inf_norm > cls.ABSOLUTE_TOLERANCE_ON_HYDRAULIC_OUTPUTS_RESIDUALS:
            res_norms = {}
            for ord_ in (1, 2):
                res_norms[ord_] = np.linalg.norm(residuals, ord=ord_)
            error_message = \
                'Inf. norm on residuals from outputs after convergence ({}) greater than permitted absolute ' \
                'tolerance ({}). Other computed norms are: {}.'.format(
                    res_inf_norm, cls.ABSOLUTE_TOLERANCE_ON_HYDRAULIC_OUTPUTS_RESIDUALS, res_norms)
            condition_number = compute_jacobian_schur_complement_matrix_condition_number(
                previous_flows, previous_heads_at_junctions, demands_at_junctions,
                cls.fixed_parameters_needed_by_solver)
            error_message += ' Jacobian condition number is {}.'.format(condition_number)
            warnings.warn(error_message, EPSWarning)
            error_messages.append(error_message)
            status = False
        # ... then update global flag cls.never_failed from local `status` ...
        cls.never_failed &= status
        # ... then extend global container cls.hydraulic_errors from local `error_messages` ...
        cls.hydraulic_errors[-1].extend(error_messages)
        # ... then compute derived metrics ; first compute order of convergence...
        if number_of_iterations > 1:
            res_diff_inf_norms_log = np.log(np.linalg.norm(list(res_diffs_per_iteration.values()), ord=np.inf, axis=1))
            coeffs = Polynomial.fit(list(res_diffs_per_iteration.keys()), res_diff_inf_norms_log, 1)
            order_of_convergence = abs(coeffs.convert().coef[1])
        else:
            order_of_convergence = np.inf
        # ... then compute elapsed time...
        process_time = time.process_time() - start_time
        # ... then compute norms 1 and 2 on residuals (if not computed yet)
        if res_norms is None:
            res_norms = {}
            for ord_ in (1, 2):
                res_norms[ord_] = np.linalg.norm(residuals, ord=ord_)
        res_norms[np.inf] = res_inf_norm
        # ... then set dictionary of all local metrics to return
        metrics_to_return = {'status': status, 'number_of_iterations': number_of_iterations,
                             'number_of_damping_corrections': number_of_damping_corrections,
                             'residual_norms': res_norms, 'order_of_convergence': order_of_convergence,
                             'process_time': process_time}
        # ... and return new flows, new heads at junctions, and the dictionary of metrics
        return new_flows, new_heads_at_junctions, metrics_to_return

    @classmethod
    def _compute_new_heads_at_tanks_with_heun_method(
            cls, first_time_step, first_timedelta, heads_at_tanks_at_start_time, first_balanced_flows,
            first_balanced_flows_m3, first_balanced_heads_at_junctions, demands_at_junctions_at_first_time_step):
        """
        Apply Heun's method (a.k.a. "improved Euler's method" or "explicit trapezoidal rule") to compute a better
        approximation of heads at tanks at first time step (at which we don't know the correct values of flows in pipes
        yet)

        :param first_time_step: first time step of the simulation (ordinal number)
        :param first_timedelta: first time delta of the simulation (of type `datetime.timedelta`)
        :param heads_at_tanks_at_start_time: initial heads at tanks (i.e. at the start time of the simulation)
        :param first_balanced_flows: flows computed from solving balance equation at first time step (l/s)
        :param first_balanced_flows_m3: same as before but in m3/s (we pass it here because we already needed
        to computed it before)
        :param first_balanced_heads_at_junctions: heads at junctions computed from solving balance equation at first
        time step
        :param demands_at_junctions_at_first_time_step: demands at junctions at first time step
        :return: corrected flows in l/s, corrected flows in m3/s, corrected heads at junctions and corrected heads at
        tanks
        """
        # predictor step: find an initial guess of new heads at tanks using forward Euler method
        approx_new_heads_at_tanks = compute_approx_new_heads_at_tanks_with_forward_euler_method(
            cls.hydraulic_time_step_in_seconds, heads_at_tanks_at_start_time, first_balanced_flows_m3,
            cls.incidence_matrix_reduced_to_tanks, cls.tanks_inertia_inverse_matrix)
        corrected_flows, corrected_heads_at_junctions = cls._solve_balance_equation_at_current_time_step(
            first_time_step, first_timedelta, first_balanced_flows, first_balanced_heads_at_junctions,
            demands_at_junctions_at_first_time_step, approx_new_heads_at_tanks)[:2]
        corrected_flows_m3 = corrected_flows / 1000
        # corrector step: improve the initial guess using trapezoidal rule
        corrected_new_heads_at_tanks = compute_new_heads_at_tanks_with_trapezoidal_rule_method(
            cls.hydraulic_time_step_in_seconds, heads_at_tanks_at_start_time, first_balanced_flows_m3,
            corrected_flows_m3, cls.incidence_matrix_reduced_to_tanks, cls.tanks_inertia_inverse_matrix)
        # and return corrected values
        return corrected_flows, corrected_flows_m3, corrected_heads_at_junctions, corrected_new_heads_at_tanks

    @staticmethod
    def _concatenate_error_messages_per_time_step(error_messages_per_time_step):
        """
        Concatenate the list of error messages of each time step, to obtain only one (long) string of error messages per
        time step.

        Note: for any time step, if the corresponding list is empty, then add string 'None' rather than an empty string.

        :param error_messages_per_time_step: list of lists of error messages
        :return: list of error message strings, containing one string per time step
        """
        concatenated_error_message_per_time_step = []
        for curr_time_step_error_messages in error_messages_per_time_step:
            if len(curr_time_step_error_messages) == 0:
                curr_time_step_concatenated_error_message = 'None'
            else:
                curr_time_step_concatenated_error_message = ' ; '.join(curr_time_step_error_messages)
            concatenated_error_message_per_time_step.append([curr_time_step_concatenated_error_message])
        return concatenated_error_message_per_time_step


def write_report_to_csv(report, dirpath='.', float_format='%.2e'):
    if isinstance(next(iter(report)), xr.DataArray):
        report = convert_xarray_report_to_pandas_report(report)
    node_report_df, pipe_report_df = report
    pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)
    for report_df in (node_report_df, pipe_report_df):
        report_df.to_csv(os.path.join(dirpath, '{}.csv'.format(report_df.name)), na_rep='NA',
                         float_format=float_format)


def write_run_info_to_csv(run_info, dirpath='.'):
    if isinstance(next(iter(run_info.values())), xr.DataArray):
        run_info = convert_xarray_runinfo_to_pandas_runinfo(run_info)
    pathlib.Path(dirpath).mkdir(parents=True, exist_ok=True)
    for run_info in run_info.values():
        if isinstance(run_info, pd.Series):
            header = False
        else:
            header = True
        run_info.to_csv(os.path.join(dirpath, '{}.csv'.format(run_info.name)), na_rep='NA', header=header)


def convert_xarray_report_to_pandas_report(xarray_report):
    pandas_report = []
    for xarr in xarray_report:
        df = xarr.to_dataframe()
        ids = df.index.droplevel(level='vars').unique()
        df = df.unstack(level='vars')
        df = df.reindex(ids, copy=False)
        df = df.droplevel(0, axis=1)
        df.name = xarr.name
        pandas_report.append(df)
    pandas_report = tuple(pandas_report)
    return pandas_report


def convert_xarray_runinfo_to_pandas_runinfo(xarray_runinfo):
    pandas_runinfo = xarray_runinfo.copy()
    for run_info_name, run_info_xarray in xarray_runinfo.items():
        run_info_df = run_info_xarray.to_dataframe()
        run_info = run_info_df.unstack(level='vars')
        if isinstance(run_info, pd.Series):
            axis = 0
        else:
            axis = 1
        run_info = run_info.droplevel(0, axis=axis)
        run_info.name = run_info_xarray.name
        pandas_runinfo[run_info_name] = run_info
    return pandas_runinfo
