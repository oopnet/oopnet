"""Module to compute Hazen-Williams friction headlosses and their derivatives, as in Carlier (1980).

Regularization of friction headlosses and their derivatives for flows close to 0 uses respectively cubic and
quadratic polynomial approximations as in Piller (1995)."""

import numpy as np

ALPHA_HW = 1.852
"""Hazen-Williams's exponent"""

ALPHA_HW_MINUS_1 = ALPHA_HW - 1
"""Convenience coefficient often used"""

FLOW_EPSILON_FOR_REGULARIZATION_OF_FRICTION_HEADLOSSES = 1e-2
"""Small value of |q| (l/s) under which use cubic regularization of unitary friction headlosses and quadratic 
regularization of their derivatives, as in Piller (1995)"""


def compute_friction_coefficients(phi_mm, chw_m3):
    """
    Compute Hazen-Williams' pipe friction coefficients (a.k.a. unitary hydraulic resistances)

    :param phi_mm: pipe diameters (mm)
    :param chw_m3: Hazen-Williams' roughnesses for flows in m**3/s
    :return: pipe friction coefficients ((s/l)**ALPHA_HW) to be used with flows in l/s
    """
    phi_m = phi_mm / 1000
    chw_l = chw_m3 * 1000
    f = 10.666721 / (phi_m**4.871 * chw_l**ALPHA_HW)
    return f


def compute_hydraulic_resistances(f, x):
    """
    Compute pipe hydraulic resistances at positions x

    :param f: Hazen-Williams' friction coefficients for flows in l/s
    :param x: positions along pipes (m)
    :return: pipe hydraulic resistances (m*(s/l)**ALPHA_HW)
    """
    r = f * x
    return r


def compute_unregularized_reduced_unitary_friction_headlosses(q):
    """
    Compute unregularized Hazen-Williams' reduced unitary friction headlosses

    :param q: flows in pipes (l/s)
    :return: reduced unitary friction headlosses ((l / s) ** ALPHA_HW)
    """
    Jred = np.abs(q) ** ALPHA_HW_MINUS_1 * q
    return Jred


def compute_unregularized_unitary_friction_headlosses(q, f):
    """
    Compute unregularized Hazen-Williams' unitary friction headlosses, as in Carlier (1980)

    :param q: flows in pipes (l/s)
    :param f: Hazen-Williams' friction coefficients for flows in l/s
    :return: unitary friction headlosses (unitless)
    """
    Jred = compute_unregularized_reduced_unitary_friction_headlosses(q)
    J = f * Jred
    return J


def compute_unregularized_friction_headlosses_until_x(q, f, x):
    """
    Compute unregularized Hazen-Williams' friction headlosses from 0 to x in pipes, as in Carlier (1980)

    :param q: flows in pipes (l/s)
    :param f: Hazen-Williams' friction coefficients for flows in l/s
    :param x: positions in pipes (m)
    :return: friction headlosses (mH2O)
    """
    J = compute_unregularized_unitary_friction_headlosses(q, f)
    xif = J * x
    return xif


def compute_unregularized_reduced_unitary_friction_headloss_derivatives_with_respect_to_flows(q):
    """
    Compute unregularized derivatives of Hazen-Williams' reduced unitary friction headlosses with respect to flows

    :param q: flows in pipes (l/s)
    :return: reduced unitary friction headloss derivatives ((l / s) ** (ALPHA_HW-1))
    """
    dJreddq = ALPHA_HW * np.abs(q) ** ALPHA_HW_MINUS_1
    return dJreddq


def compute_unregularized_unitary_friction_headloss_derivatives_with_respect_to_flows(q, f):
    """
    Compute unregularized derivatives of Hazen-Williams' unitary friction headlosses with respect to flows

    :param q: flows in pipes (l/s)
    :param f: Hazen-Williams' friction coefficients for flows in l/s
    :return: unitary friction headloss derivatives (s/l)
    """
    dJreddq = compute_unregularized_reduced_unitary_friction_headloss_derivatives_with_respect_to_flows(q)
    dJdq = f * dJreddq
    return dJdq


def compute_unregularized_friction_headloss_derivatives_with_respect_to_flows_until_x(q, f, x):
    """
    Compute unregularized derivatives of Hazen-Williams' friction headlosses integrated from 0 to x with respect to
    flows

    :param q: flows in pipes (l/s)
    :param f: Hazen-Williams' friction coefficients for flows in l/s
    :param x: positions in pipes (m)
    :return: derivatives of friction headlosses (mH2O s/l)
    """
    dJdq = compute_unregularized_unitary_friction_headloss_derivatives_with_respect_to_flows(q, f)
    dxifdq = dJdq * x
    return dxifdq


def compute_cubic_polynomial_approximation_residuals_for_flows_close_to_zero(coeffs):
    """
    System of equations to solve to find the cubic polynomial regularization of the reduced unitary friction headlosses
    (i.e. unitary friction headlosses with f = 1), for |q| <= eps, as in Piller (1995).
    Note: this function shares the same interface as parameter `func` of function `scipy.optimize.root`

    :param coeffs: the polynomial coefficients to find, in order of increasing degree
    :return: residuals obtained from coefficients `coeffs`
    """
    eps = FLOW_EPSILON_FOR_REGULARIZATION_OF_FRICTION_HEADLOSSES
    a1, a3 = coeffs
    eps_arr = np.array([eps])
    function_continuity_at_zero_plus_eps = \
        a3 * eps ** 3 + a1 * eps - compute_unregularized_reduced_unitary_friction_headlosses(eps_arr).item()
    derivative_continuity_at_zero_plus_eps = \
        3 * a3 * eps ** 2 + a1 \
        - compute_unregularized_reduced_unitary_friction_headloss_derivatives_with_respect_to_flows(eps_arr).item()
    residuals = [function_continuity_at_zero_plus_eps, derivative_continuity_at_zero_plus_eps]
    return residuals


def compute_regularized_reduced_unitary_friction_headlosses(q, p):
    """
    Compute regularized Hazen-Williams's reduced unitary friction headlosses in pipes

    :param q: flows in pipes (l/s)
    :param p: cubic polynomial used to regularized reduced unitary friction headlosses for low flows
    :return: regularized Hazen-Williams's reduced unitary friction headlosses ((l / s) ** ALPHA_HW)
    """
    eps = FLOW_EPSILON_FOR_REGULARIZATION_OF_FRICTION_HEADLOSSES
    Jred_reg = np.empty_like(q)
    toreg_msk = np.abs(q) <= eps  # low |q| mask
    Jred_reg[toreg_msk] = p(q[toreg_msk])
    norm_msk = ~toreg_msk  # normal |q| mask
    Jred_reg[norm_msk] = compute_unregularized_reduced_unitary_friction_headlosses(q[norm_msk])
    return Jred_reg


def compute_regularized_unitary_friction_headlosses(q, f, p):
    """
    Compute regularized Hazen-Williams's unitary friction headlosses in pipes, as in Piller (1995)

    :param q: flows in pipes (l/s)
    :param f: Hazen-Williams' friction coefficients for flows in l/s
    :param p: cubic polynomial used to regularized reduced unitary friction headlosses for low flows
    :return: regularized Hazen-Williams's unitary friction headlosses (unitless)
    """
    eps = FLOW_EPSILON_FOR_REGULARIZATION_OF_FRICTION_HEADLOSSES
    Jreg = np.empty_like(q)
    toreg_msk = np.abs(q) <= eps  # low |q| mask
    Jred_reg = compute_regularized_reduced_unitary_friction_headlosses(q[toreg_msk], p)
    Jreg[toreg_msk] = f[toreg_msk] * Jred_reg
    norm_msk = ~toreg_msk  # normal |q| mask
    Jreg[norm_msk] = compute_unregularized_unitary_friction_headlosses(q[norm_msk], f[norm_msk])
    return Jreg


def compute_regularized_friction_headlosses_until_x(q, f, x, p):
    """
    Compute regularized Hazen-Williams's friction headlosses from 0 to x in pipes, as in Piller (1995)

    :param q: flows in pipes (l/s)
    :param f: Hazen-Williams' friction coefficients for flows in l/s
    :param x: positions in pipes (m)
    :param p: cubic polynomial used to regularized reduced unitary friction headlosses for low flows
    :return: regularized Hazen-Williams's friction headlosses (mH2O)
    """
    Jreg = compute_regularized_unitary_friction_headlosses(q, f, p)
    xifreg = Jreg * x
    return xifreg


def compute_regularized_reduced_unitary_friction_headloss_derivatives_with_respect_to_flows(q, p):
    """
    Compute derivatives of Hazen-Williams' regularized reduced unitary friction headlosses with respect to flows

    :param q: flows in pipes (l/s)
    :param p: quadratic polynomial used to regularized reduced unitary friction headloss derivatives for low flows
    :return: derivatives of regularized Hazen-Williams's reduced unitary friction headlosses (s/l)
    """
    eps = FLOW_EPSILON_FOR_REGULARIZATION_OF_FRICTION_HEADLOSSES
    dJregreddq = np.empty_like(q)
    toreg_msk = np.abs(q) <= eps  # low |q| mask
    dJregreddq[toreg_msk] = p(q[toreg_msk])
    norm_msk = ~toreg_msk  # normal |q| mask
    dJregreddq[norm_msk] = compute_unregularized_reduced_unitary_friction_headloss_derivatives_with_respect_to_flows(
        q[norm_msk])
    return dJregreddq


def compute_regularized_unitary_friction_headloss_derivatives_with_respect_to_flows(q, f, p):
    """
    Compute derivatives of Hazen-Williams' regularized unitary friction headlosses with respect to flows, as in
    Piller (1995)

    :param q: flows in pipes (l/s)
    :param f: Hazen-Williams' friction coefficients for flows in l/s
    :param p: quadratic polynomial used to regularized reduced unitary friction headloss derivatives for low flows
    :return: derivatives of regularized Hazen-Williams's unitary friction headlosses (s/l)
    """
    eps = FLOW_EPSILON_FOR_REGULARIZATION_OF_FRICTION_HEADLOSSES
    dJregdq = np.empty_like(q)
    toreg_msk = np.abs(q) <= eps  # low |q| mask
    dJregreddq = compute_regularized_reduced_unitary_friction_headloss_derivatives_with_respect_to_flows(
        q[toreg_msk], p)
    dJregdq[toreg_msk] = f[toreg_msk] * dJregreddq
    norm_msk = ~toreg_msk  # normal |q| mask
    dJregdq[norm_msk] = compute_unregularized_unitary_friction_headloss_derivatives_with_respect_to_flows(
        q[norm_msk], f[norm_msk])
    return dJregdq


def compute_regularized_friction_headloss_derivatives_with_respect_to_flows_until_x(q, f, x, p):
    """
    Compute derivatives of Hazen-Williams' regularized friction headlosses integrated from 0 to x with respect to
    flows, as in Piller (1995)

    :param q: flows in pipes (l/s)
    :param f: Hazen-Williams' friction coefficients for flows in l/s
    :param x: positions in pipes (m)
    :param p: quadratic polynomial used to regularized reduced unitary friction headloss derivatives for low flows
    :return: derivatives of regularized Hazen-Williams's friction headlosses (m/l/s)
    """
    dJregdq = compute_regularized_unitary_friction_headloss_derivatives_with_respect_to_flows(q, f, p)
    dxifdq_reg = dJregdq * x
    return dxifdq_reg


def compute_friction_headlosses_per_1000m(xif, l):
    """
    Compute pipe friction headlosses per 1000 m

    :param xif: pipe friction headlosses (m)
    :param l: pipe lengths (m)
    :return: pipe friction headlosses per 1000 m (m)
    """
    xifper1000m = xif / l * 1000
    return xifper1000m
