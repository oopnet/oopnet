"""Module to compute parameters derived from pipe attributes."""

from math import pi


def compute_cross_sectional_areas(phi_mm):
    """
    Compute cross sectional areas of pipes

    :param phi_mm: pipe diameters (mm)
    :return: cross sectional areas of pipes (m2)
    """
    phi_m = phi_mm / 1000
    r = phi_m / 2
    return pi * r ** 2
