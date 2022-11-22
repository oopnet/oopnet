"""Module to compute PDM consumptions and their derivatives from pressure fractions at junctions, using function POR
from Wagner et al. (1988).
Regularization of consumptions and their derivatives for pressure fractions close to 0 or 1 uses respectively cubic and
quadratic polynomial approximations, as in Piller et al. (2003)."""

import numpy as np

MINIMUM_PRESSURE_HEAD_AT_JUNCTIONS = 0
"""Minimum pressure head at junctions (mH2O)"""

SERVICE_PRESSURE_HEAD_AT_JUNCTIONS = 20
"""Service pressure head at junctions (mH2O)"""

PRESSURE_FRACTION_EPSILON_FOR_REGULARIZATION_OF_UNITARY_CONSUMPTIONS_AT_JUNCTIONS = 1e-3
"""Small (unitless) value used to define the intervals {z | abs(z) <= eps} and {z | abs(z - 1) <= eps} into 
which unitary consumptions and their derivatives will be regularized by respectively cubic and quadratic polynomials, as 
in Piller et al. (2003)"""


def compute_pressure_fractions(h, u):
    """
    Compute pressure fractions at junctions, as in Wagner et al. (1988)

    :param h: heads at junctions (mH2O)
    :param u: elevations at junctions (m)
    :return: pressure fractions at junctions (unitless)
    """
    hpm = MINIMUM_PRESSURE_HEAD_AT_JUNCTIONS
    hps = SERVICE_PRESSURE_HEAD_AT_JUNCTIONS
    z = (h - (hpm + u)) / (hps - hpm)
    return z


def compute_pressure_fraction_derivative():
    """
    Compute derivative of pressure fractions at junctions with respect to heads

    :return: derivative of pressure fractions at junctions (/mH2O) ; same value for all junctions
    """
    hpm = MINIMUM_PRESSURE_HEAD_AT_JUNCTIONS
    hps = SERVICE_PRESSURE_HEAD_AT_JUNCTIONS
    dzdh = 1 / (hps - hpm)
    return dzdh


def _compute_unregularized_unitary_consumptions(z):
    """
    Compute unregularized unitary consumptions at junctions, as in Wagner et al. (1988)

    :param z: pressure fractions at junctions (unitless)
    :return: unitary consumptions at junctions (unitless)
    """
    uc = np.empty_like(z)
    unsupp_msk = np.isclose(z, 0) | (z < 0)
    fullsupp_msk = np.isclose(z, 1) | (z > 1)
    partsupp_msk = ~unsupp_msk & ~fullsupp_msk
    uc[unsupp_msk] = 0
    uc[fullsupp_msk] = 1
    uc[partsupp_msk] = np.sqrt(z[partsupp_msk])
    return uc


def _compute_unregularized_unitary_consumption_derivatives_with_respect_to_pressure_fractions(z):
    """
    Compute unregularized derivatives of unitary consumptions at junctions with respect to pressure fractions

    :param z: pressure fractions at junctions (unitless)
    :return: derivatives of unitary consumptions at junctions with respect to pressure fractions (unitless)
    """
    ducdz = np.empty_like(z)
    unsupp_msk = np.isclose(z, 0) | (z < 0)
    fullsupp_msk = np.isclose(z, 1) | (z > 1)
    partsupp_msk = ~unsupp_msk & ~fullsupp_msk
    ducdz[partsupp_msk] = 1 / (2 * np.sqrt(z[partsupp_msk]))
    ducdz[~partsupp_msk] = 0
    return ducdz


def _compute_unregularized_unitary_consumption_derivatives_with_respect_to_heads(z, dzdh):
    """
    Compute unregularized derivatives of unitary consumptions at junctions with respect to heads

    :param z: pressure fractions at junctions (unitless)
    :param dzdh: derivative of pressure fractions at junctions (/mH2O) ; same value for all junctions
    :return: derivatives of unitary consumptions at junctions with respect to heads (/mH2O)
    """
    ducdz = _compute_unregularized_unitary_consumption_derivatives_with_respect_to_pressure_fractions(z)
    ducdh = ducdz * dzdh
    return ducdh


def compute_cubic_polynomial_approximation_residuals_for_pressure_fractions_close_to_zero(coeffs):
    """
    System of equations to solve to find the cubic polynomial regularization of the unitary consumptions at junctions
    where abs(z) <= eps, as in Piller et al. (2003).
    Note: this function shares the same interface as parameter `func` of function `scipy.optimize.root`

    :param coeffs: the polynomial coefficients to find, in order of increasing degree
    :return: residuals obtained from coefficients `coeffs`
    """
    eps = PRESSURE_FRACTION_EPSILON_FOR_REGULARIZATION_OF_UNITARY_CONSUMPTIONS_AT_JUNCTIONS
    a0, a1, a2, a3 = coeffs
    eps_arr = np.array([eps])
    function_continuity_at_zero_minus_eps = - a3 * eps ** 3 + a2 * eps ** 2 - a1 * eps + a0
    function_continuity_at_zero_plus_eps = \
        a3 * eps ** 3 + a2 * eps ** 2 + a1 * eps + a0 - _compute_unregularized_unitary_consumptions(eps_arr).item()
    derivative_continuity_at_zero_minus_eps = 3 * a3 * eps ** 2 - 2 * a2 * eps + a1
    derivative_continuity_at_zero_plus_eps = \
        3 * a3 * eps ** 2 + 2 * a2 * eps + a1 \
        - _compute_unregularized_unitary_consumption_derivatives_with_respect_to_pressure_fractions(eps_arr).item()
    residuals = [function_continuity_at_zero_minus_eps, function_continuity_at_zero_plus_eps,
                 derivative_continuity_at_zero_minus_eps, derivative_continuity_at_zero_plus_eps]
    return residuals


def compute_cubic_polynomial_approximation_residuals_for_pressure_fractions_close_to_one(coeffs):
    """
    System of equations to solve to find the cubic polynomial regularization of the unitary consumptions at junctions
    where abs(z - 1) <= eps, as in Piller et al. (2003).
    Note: this function shares the same interface as parameter `func` of function `scipy.optimize.root`

    :param coeffs: the polynomial coefficients to find, in order of increasing degree
    :return: residuals obtained from coefficients `coeffs`
    """
    eps = PRESSURE_FRACTION_EPSILON_FOR_REGULARIZATION_OF_UNITARY_CONSUMPTIONS_AT_JUNCTIONS
    one_minus_eps = 1 - eps
    one_minus_eps_arr = np.array([one_minus_eps])
    one_plus_eps = 1 + eps
    a0, a1, a2, a3 = coeffs
    function_continuity_at_one_minus_eps = \
        a3 * one_minus_eps ** 3 + a2 * one_minus_eps ** 2 + a1 * one_minus_eps + a0 \
        - _compute_unregularized_unitary_consumptions(one_minus_eps_arr).item()
    function_continuity_at_one_plus_eps = a3 * one_plus_eps ** 3 + a2 * one_plus_eps ** 2 + a1 * one_plus_eps + a0 - 1
    derivative_continuity_at_one_minus_eps = \
        3 * a3 * one_minus_eps ** 2 + 2 * a2 * one_minus_eps + a1 \
        - _compute_unregularized_unitary_consumption_derivatives_with_respect_to_pressure_fractions(
            one_minus_eps_arr).item()
    derivative_continuity_at_one_plus_eps = 3 * a3 * one_plus_eps ** 2 + 2 * a2 * one_plus_eps + a1
    residuals = [function_continuity_at_one_minus_eps, function_continuity_at_one_plus_eps,
                 derivative_continuity_at_one_minus_eps, derivative_continuity_at_one_plus_eps]
    return residuals


def compute_regularized_unitary_consumptions(z, p0, p1):
    """
    Compute the 2-side regularized unitary consumptions at junctions, as in Piller et al. (2003)

    :param z: pressure fractions at junctions (unitless)
    :param p0: cubic polynomial used to regularized the unitary consumptions for abs(z) <= eps
    :param p1: same as p0 but for abs(z - 1) <= eps
    :return: regularized unitary consumptions at junctions
    """
    eps = PRESSURE_FRACTION_EPSILON_FOR_REGULARIZATION_OF_UNITARY_CONSUMPTIONS_AT_JUNCTIONS
    ds_reg = np.empty_like(z)
    reg0_msk = np.abs(z) <= eps
    reg1_msk = np.abs(z-1) <= eps
    ds_reg[reg0_msk] = p0(z[reg0_msk])
    ds_reg[reg1_msk] = p1(z[reg1_msk])
    norm_msk = ~reg0_msk & ~reg1_msk
    ds_reg[norm_msk] = _compute_unregularized_unitary_consumptions(z[norm_msk])
    return ds_reg


def _compute_regularized_unitary_consumption_derivatives_with_respect_to_pressure_fractions(z, p0, p1):
    """
    Compute the derivatives of the 2-side regularized unitary consumptions at junctions with respect to pressure
    fractions, as in Piller et al. (2003)

    :param z: pressure fractions at junctions (unitless)
    :param p0: quadratic polynomial used to regularized the unitary consumption derivatives with respect to pressure
    fractions for abs(z) <= eps
    :param p1: same as p0 but for abs(z - 1) <= eps
    :return: derivatives, with respect to pressure fractions, of regularized unitary consumptions at junctions (unit-
    less)
    """
    eps = PRESSURE_FRACTION_EPSILON_FOR_REGULARIZATION_OF_UNITARY_CONSUMPTIONS_AT_JUNCTIONS
    ducdz_reg = np.empty_like(z)
    reg0_msk = np.abs(z) <= eps
    reg1_msk = np.abs(z - 1) <= eps
    ducdz_reg[reg0_msk] = p0(z[reg0_msk])
    ducdz_reg[reg1_msk] = p1(z[reg1_msk])
    norm_msk = ~reg0_msk & ~reg1_msk
    ducdz_reg[norm_msk] = _compute_unregularized_unitary_consumption_derivatives_with_respect_to_pressure_fractions(
        z[norm_msk])
    return ducdz_reg


def compute_regularized_unitary_consumption_derivatives_with_respect_to_heads(z, p0, p1, dzdh):
    """
    Compute the derivatives of the 2-side regularized unitary consumptions at junctions with respect to heads

    :param z: pressure fractions at junctions (unitless)
    :param p0: quadratic polynomial used to regularized the unitary consumption derivatives with respect to pressure
    fractions for abs(z) <= eps
    :param p1: same as p0 but for abs(z - 1) <= eps
    :param dzdh: derivative of pressure fractions at junctions (/mH2O) ; same value for all junctions
    :return: derivatives, with respect to heads, of regularized unitary consumptions at junctions (/mH2O)
    """
    ducdz_reg = _compute_regularized_unitary_consumption_derivatives_with_respect_to_pressure_fractions(z, p0, p1)
    ducdh_reg = ducdz_reg * dzdh
    return ducdh_reg


def compute_consumptions(uc, d):
    """
    Compute consumptions at junctions

    :param uc: unitary consumptions at junctions (unitless)
    :param d: demands at junctions (l/s)
    :return: consumptions at junctions (l/s)
    """
    c = uc * d
    return c


def compute_consumption_derivatives_with_respect_to_heads(ducdh, d):
    """
    Compute derivatives of consumptions at junctions with respect to heads

    :param ducdh: derivatives with respect to heads of unitary consumptions at junctions (/mH2O)
    :param d: demands at junctions (l/s)
    :return: consumption derivatives at junctions (l/s/mH2O)
    """
    dcdh = ducdh * d
    return dcdh
