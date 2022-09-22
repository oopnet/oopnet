"""Module to interpolate the demands at any time of the time grid, calling function scipy.interpolate.PchipInterpolator.
"""


import numpy as np
from scipy import interpolate


def compute_interpolators_of_the_demands_at_junctions(
        nominal_demands, global_demand_multiplier, demand_patterns, default_demand_pattern, pattern_timestep_in_seconds,
        pattern_start_in_seconds, simulation_duration_in_seconds):
    """
    Compute interpolators of the demands at junctions

    :param nominal_demands: see oopnet.elements.network_components.Junction.demand
    :param global_demand_multiplier: see oopnet.elements.network.options.demandmultiplier
    :param demand_patterns: see oopnet.elements.network_components.Junction.demandpattern
    :param pattern_timestep_in_seconds: see oopnet.elements.network.times.patterntimestep
    :param pattern_start_in_seconds: see oopnet.elements.network.times.patternstart
    :param simulation_duration_in_seconds: see oopnet.elements.network.times.duration
    :return: interpolators to compute the demands (l/s) over the simulation time grid
    """
    interpolation_time_grid_length = int(simulation_duration_in_seconds / pattern_timestep_in_seconds) + 1
    interpolation_time_grid = np.linspace(
        pattern_start_in_seconds, simulation_duration_in_seconds + pattern_start_in_seconds,
        interpolation_time_grid_length)
    demand_interpolators = []

    # patterns of demands at junctions
    for i, demand_pattern in enumerate(demand_patterns):
        if isinstance(demand_pattern, list):
            demand_pattern_list = demand_pattern
            for j, demand_pattern_ in enumerate(demand_pattern_list):
                if demand_pattern_ is None:
                    demand_pattern_list[j] = default_demand_pattern
        else:
            if demand_pattern is None:
                demand_patterns[i] = default_demand_pattern

    for nominal_demand, demand_pattern in zip(nominal_demands, demand_patterns):

        if isinstance(nominal_demand, list):  # multiple demand categories
            nominal_demand = nominal_demand[1:]
        nominal_demand_array = np.atleast_1d(nominal_demand) * global_demand_multiplier

        if isinstance(demand_pattern, list):  # multiple demand patterns
            demand_pattern_list = demand_pattern[1:]
        else:
            demand_pattern_list = [demand_pattern]

        demand_over_interpolation_time_grid = np.zeros_like(interpolation_time_grid)
        for (nominal_demand_, demand_pattern_) in zip(nominal_demand_array, demand_pattern_list):
            demand_over_interpolation_time_grid += nominal_demand_ * np.resize(
                    demand_pattern_.multipliers, interpolation_time_grid_length)

        if len(interpolation_time_grid) == 1:
            demand_interpolator = ConstantDemandFunction(demand_over_interpolation_time_grid.item(0))
        else:
            demand_interpolator = interpolate.PchipInterpolator(
                interpolation_time_grid, demand_over_interpolation_time_grid)

        demand_interpolators.append(demand_interpolator)

    return demand_interpolators


class ConstantDemandFunction:
    """
    Callable class to return a constant demand, providing the same interface as non-constant interpolators.
    """
    def __init__(self, constant_demand):
        """
        :param constant_demand: constant demand to return everytime the instance is called (l/s)
        """
        self.constant_demand = constant_demand

    def __call__(self, _):
        """
        :param _: not used
        :return: constant demand (l/s)
        """
        return self.constant_demand


def interpolate_demands_from_interpolators(time_in_seconds, interpolators):
    """
    Interpolate the demand at each junction at the given time using interpolators passed as argument

    :param time_in_seconds: the time at which to interpolate the demands (s)
    :param interpolators: list of interpolators ; each of them takes a time as parameter
    :return: interpolated demands at junctions (l/s)
    """
    interpolated_values = []
    for interpolator in interpolators:
        interpolated_values.append(interpolator(time_in_seconds))
    return np.array(interpolated_values)
