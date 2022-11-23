"""Module to compute velocities from flows and flows from velocities in pipes."""


def compute_velocities_from_flows(q_l, csa):
    """
    Compute velocities of flows in pipes

    :param q_l: flows in pipes (l/s)
    :param csa: pipe cross sectional areas (m2)
    :return: flow velocities (m/s)
    """
    q_m3 = q_l / 1000
    v = q_m3 / csa
    return v


def compute_flows_from_velocities(v, csa):
    """
    Compute flows from velocities in pipes

    :param v: flow velocities (m/s)
    :param csa: pipe cross sectional areas (m2)
    :return: flows in pipes (l/s)
    """
    qm3 = v * csa
    ql = qm3 * 1000
    return ql
