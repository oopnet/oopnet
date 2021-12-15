# Retrieve all id's of specific objects
from oopnet.elements.network import Network


def get_pattern_ids(network: Network) -> list:
    """Function for getting all pattern ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of pattern ids

    """
    return list(network.patterns.keys())


def get_curve_ids(network: Network) -> list:
    """Function for getting all curve ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of curve ids

    """
    return list(network.curves.keys())


def get_rule_ids(network: Network) -> list:
    """Function for getting all rule ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of curve ids

    """
    return list(network.rules.keys())


def get_junction_ids(network: Network) -> list:
    """Function for getting all junction ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of junction ids

    """
    return list(network.junctions.keys())


def get_tank_ids(network: Network) -> list:
    """Function for getting all tank ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of tank ids

    """
    return list(network.tanks.keys())


def get_reservoir_ids(network: Network) -> list:
    """Function for getting all reservoir ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of reservoir ids

    """
    return list(network.reservoirs.keys())


def get_node_ids(network: Network) -> list:
    """Function for getting all node ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of node ids

    """
    return get_junction_ids(network) + get_tank_ids(network) + get_reservoir_ids(network)


def get_pipe_ids(network: Network) -> list:
    """Function for getting all pipe ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of pipe ids

    """
    return list(network.pipes.keys())


def get_pump_ids(network: Network) -> list:
    """Function for getting all pump ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of pump ids

    """
    return list(network.pumps.keys())


def get_valve_ids(network: Network) -> list:
    """Function for getting all valve ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of valve ids

    """
    return list(network.valves.keys())


def get_link_ids(network: Network) -> list:
    """Function for getting all link ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of link ids

    """
    return get_pipe_ids(network) + get_pump_ids(network) + get_valve_ids(network)


# Retrieve all specific objects
def get_pipes(network: Network) -> list:
    """This function returns all network pipes as a list

    Args:
      network: OOPNET network object

    Returns:
      list of pipes

    """
    return list(network.pipes.values())


def get_junctions(network: Network) -> list:
    """This function returns all network junctions as a list

    Args:
      network: OOPNET network object

    Returns:
      list of junctions

    """
    return list(network.junctions.values())


def get_reservoirs(network: Network) -> list:
    """This function returns all reservoirs in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of reservoirs

    """
    return list(network.reservoirs.values())


def get_tanks(network: Network) -> list:
    """This function returns all tanks in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of tanks

    """
    return list(network.tanks.values())


def get_nodes(network: Network) -> list:
    """This function returns all network nodes as a list (junctions, tanks and reservoirs)

    Args:
      network: OOPNET network object

    Returns:
      list of nodes

    """
    return get_junctions(network) + get_tanks(network) + get_reservoirs(network)


def get_links(network: Network) -> list:
    """This function returns all network links as a list (pipes, pumps and valves)

    Args:
      network: OOPNET network object

    Returns:
      list of links

    """
    return get_pipes(network) + get_pumps(network) + get_valves(network)


def get_pumps(network: Network) -> list:
    """This function returns all pumps in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of pumps

    """
    return list(network.pumps.values())


def get_valves(network: Network) -> list:
    """This function returns all valves in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of valves

    """
    return list(network.valves.values())


def get_curves(network: Network) -> list:
    """This function returns all curves in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of curves

    """
    return list(network.curves.values())


def get_patterns(network: Network) -> list:
    """This function returns all patterns in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of patterns

    """
    return list(network.patterns.values())


def get_energies(network: Network) -> list:
    """This function returns all energy entries in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of energy entries

    """
    return network.energies


def get_controls(network: Network) -> list:
    """This function returns all controls in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of controls

    """
    return network.controls


def get_rules(network: Network) -> list:
    """This function returns all rules in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of rules

    """
    return list(network.rules.values())
