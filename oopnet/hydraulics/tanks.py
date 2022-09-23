"""Module to compute parameters derived from tank attributes."""


from scipy import sparse

from math import pi


def compute_cross_sectional_areas(phi):
    """
    Compute cross sectional areas of tanks.
    Note: we suppose tanks are cylindrical

    :param phi: tank diameters (m)
    :return: cross sectional areas of tanks (m2)
    """
    r = phi / 2
    sf = pi * r ** 2
    return sf


def compute_inertia_matrix(sf):
    """
    Compute diagonal matrix of tanks inertia

    :param sf: tank cross sectional areas (m2)
    :return: tanks inertia diagonal matrix (m2)
    """
    Sf = sparse.diags(sf)
    return Sf
