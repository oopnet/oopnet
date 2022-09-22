
import numpy as np


class SolverException(Exception):
    """
    Base class for any exception raised from current package.
    """
    pass


class SolverWarning(Warning):
    """
    Base class for any warning issued from current package.
    """
    pass


def compute_headlosses_from_source_nodes(
        number_of_pipes, heads_at_tanks, heads_at_reservoirs, incidence_matrix_reduced_to_tanks,
        incidence_matrix_reduced_to_reservoirs):
    """
    Compute the contribution of sources (i.e. tanks and reservoirs) nodes in the resulting headlosses along pipes.

    :param number_of_pipes: number of pipes
    :param heads_at_tanks: heads at tanks (mH2O)
    :param heads_at_reservoirs: heads at reservoirs (mH2O)
    :param incidence_matrix_reduced_to_tanks: incidence matrix reduced to tanks
    :param incidence_matrix_reduced_to_reservoirs: incidence matrix reduced to reservoirs
    :return: the contribution of sources nodes in the resulting headlosses along pipes (mH2O).
    """
    headlosses_from_source_nodes = np.zeros(number_of_pipes, dtype=float)
    if heads_at_tanks is not None:
        tanks_head_deltas = incidence_matrix_reduced_to_tanks.T @ heads_at_tanks
        headlosses_from_source_nodes += tanks_head_deltas
    if heads_at_reservoirs is not None:
        reservoirs_head_deltas = incidence_matrix_reduced_to_reservoirs.T @ heads_at_reservoirs
        headlosses_from_source_nodes += reservoirs_head_deltas
    return headlosses_from_source_nodes


def compute_energy_residuals_in_pipes(
        friction_headlosses, heads_at_junctions, headlosses_from_source_nodes, incidence_matrix_reduced_to_junctions):
    """
    Compute energy residuals in pipes

    :param friction_headlosses: friction headlosses along pipes
    :param heads_at_junctions: heads at junctions
    :param headlosses_from_source_nodes: contribution of sources nodes in the resulting headlosses along pipes (mH2O)
    :param incidence_matrix_reduced_to_junctions: incidence matrix reduced to junction nodes
    :return: energy residuals (mH2O)
    """
    return \
        friction_headlosses - incidence_matrix_reduced_to_junctions.T @ heads_at_junctions \
        - headlosses_from_source_nodes


def compute_mass_residuals_at_junctions(flows_in_pipes, outflows_at_junctions, incidence_matrix_reduced_to_junctions):
    """
    Compute mass residuals at junctions

    :param flows_in_pipes: flows in pipes (l/s)
    :param outflows_at_junctions: total outflows at junctions (l/s)
    :param incidence_matrix_reduced_to_junctions: incidence matrix reduced to junction nodes
    :return: mass residuals (l/s)
    """
    return - incidence_matrix_reduced_to_junctions @ flows_in_pipes - outflows_at_junctions
