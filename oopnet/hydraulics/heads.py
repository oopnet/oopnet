"""Module to compute variables derived from heads, pressure heads and elevations at nodes."""


def compute_heads_from_pressure_heads(hp, u):
    """
    Compute heads from pressure heads and elevations at nodes

    :param hp: pressure heads (mH2O)
    :param u: elevation (m)
    :return: heads (mH2O)
    """
    return u + hp


def compute_pressure_heads_from_heads(h, u):
    """
    Compute pressure heads from heads at nodes

    :param h: heads (m)
    :param u: elevations (m)
    :return: pressure heads (m)
    """
    hp = h - u
    return hp
