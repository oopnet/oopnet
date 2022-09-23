"""Module to compute velocities in pipes."""


def compute_velocities(q_l, sp):
    """
    Compute velocities of flows in pipes

    :param q_l: flows in pipes (l/s)
    :param sp: pipe cross sectional areas (m2)
    :return: flow velocities (m/s)
    """
    q_m3 = q_l / 1000
    v = q_m3 / sp
    return v
