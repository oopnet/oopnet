

def compute_approx_new_heads_at_tanks_with_forward_euler_method(
        hydraulic_time_step_in_seconds, previous_heads_at_tanks, new_flows_m3, incidence_matrix_reduced_to_tanks,
        tanks_inertia_inverse_matrix):
    """
    Compute new roughly approximated heads at tanks using forward Euler method (explicit first-order method).

    This method can be used as predictor step, before using trapezoidal rule through function
    `compute_new_heads_at_tanks_with_trapezoidal_rule_method`.

    :param hydraulic_time_step_in_seconds: hydraulic time step used for the integration of heads at tanks (s)
    :param previous_heads_at_tanks: heads at tanks computed at previous time step (mH2O)
    :param new_flows_m3: flows in pipes computed at current time step (m3/s)
    :param incidence_matrix_reduced_to_tanks: incidence matrix reduced to tanks
    :param tanks_inertia_inverse_matrix: inverse of the inertia matrix of tanks
    :return: new approximated heads at tanks
    """
    new_heads_at_tanks = \
        previous_heads_at_tanks - hydraulic_time_step_in_seconds \
        * tanks_inertia_inverse_matrix @ incidence_matrix_reduced_to_tanks * new_flows_m3
    return new_heads_at_tanks


def compute_new_heads_at_tanks_with_trapezoidal_rule_method(
        hydraulic_time_step_in_seconds, previous_heads_at_tanks, previous_flows_m3, new_flows_m3,
        incidence_matrix_reduced_to_tanks, tanks_inertia_inverse_matrix):
    """
    Compute new heads at tanks using trapezoidal rule method (implicit second-order method).

    This method requires to know both previous and current flows in pipes. If previous flows are unknown, one can
    approximate them using function `compute_approx_new_heads_at_tanks_with_forward_euler_method`.

    :param hydraulic_time_step_in_seconds: hydraulic time step used for the integration of heads at tanks (s)
    :param previous_heads_at_tanks: heads at tanks computed at previous time step (mH2O)
    :param previous_flows_m3: flows in pipes in m3/s computed at previous time step (m3/s)
    :param new_flows_m3: flows in pipes computed at current time step (m3/s)
    :param incidence_matrix_reduced_to_tanks: incidence matrix reduced to tanks
    :param tanks_inertia_inverse_matrix: inverse of the inertia matrix of tanks
    :return: new heads at tanks
    """
    new_heads_at_tanks = \
        previous_heads_at_tanks - 0.5 * hydraulic_time_step_in_seconds \
        * tanks_inertia_inverse_matrix @ incidence_matrix_reduced_to_tanks \
        * (previous_flows_m3 + new_flows_m3)
    return new_heads_at_tanks
