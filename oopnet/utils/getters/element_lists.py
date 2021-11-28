# Retrieve all id's of specific objects
from oopnet.elements.network import Network, ComponentList


def get_pattern_ids(network: Network) -> list:
    """Function for getting all pattern ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of pattern ids

    """
    return [x.id for x in network.patterns]


def get_curve_ids(network: Network) -> list:
    """Function for getting all curve ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of curve ids

    """
    return [x.id for x in network.curves]


def get_junction_ids(network: Network) -> list:
    """Function for getting all junction ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of junction ids

    """
    return [x.id for x in network.junctions]


def get_tank_ids(network: Network) -> list:
    """Function for getting all tank ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of tank ids

    """
    return [x.id for x in network.tanks]


def get_reservoir_ids(network: Network) -> list:
    """Function for getting all reservoir ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of reservoir ids

    """
    return [x.id for x in network.reservoirs]


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
    return [x.id for x in network.pipes]


def get_pump_ids(network: Network) -> list:
    """Function for getting all pump ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of pump ids

    """
    return [x.id for x in network.pumps]


def get_valve_ids(network: Network) -> list:
    """Function for getting all valve ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of valve ids

    """
    return [x.id for x in network.valves]


def get_link_ids(network: Network) -> list:
    """Function for getting all link ids in a network

    Args:
      network: OOPNET network object

    Returns:
      list of link ids

    """
    return get_pipe_ids(network) + get_pump_ids(network) + get_valve_ids(network)


# Retrieve all specific objects
def get_pipes(network: Network) -> ComponentList:
    """This function returns all network pipes as a list

    Args:
      network: OOPNET network object

    Returns:
      list of pipes

    """
    return network.pipes


def get_junctions(network: Network) -> ComponentList:
    """This function returns all network junctions as a list

    Args:
      network: OOPNET network object

    Returns:
      list of junctions

    """
    return network.junctions


def get_reservoirs(network: Network) -> ComponentList:
    """This function returns all reservoirs in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of reservoirs

    """
    return network.reservoirs


def get_tanks(network: Network) -> ComponentList:
    """This function returns all tanks in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of tanks

    """
    return network.tanks


def get_nodes(network: Network) -> ComponentList:
    """This function returns all network nodes as a list (junctions, tanks and reservoirs)

    Args:
      network: OOPNET network object

    Returns:
      list of nodes

    """
    return network.junctions + network.tanks + network.reservoirs


def get_links(network: Network) -> ComponentList:
    """This function returns all network links as a list (pipes, pumps and valves)

    Args:
      network: OOPNET network object

    Returns:
      list of links

    """
    return network.pipes + network.pumps + network.valves


def get_pumps(network: Network) -> ComponentList:
    """This function returns all pumps in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of pumps

    """
    return network.pumps


def get_valves(network: Network) -> ComponentList:
    """This function returns all valves in the network as a list

    Args:
      network: OOPNET network object

    Returns:
      list of valves

    """
    return network.valves
