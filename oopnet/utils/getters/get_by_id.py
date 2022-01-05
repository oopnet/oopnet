from oopnet.elements import Network, Junction, Link, Node, Valve, Pump, Pipe, Reservoir, Tank, Rule, Pattern, Curve


def get_junction(network: Network, id: str) -> Junction:
    """This function returns a specific Junction from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Junction

    Returns:
      Junction with property id

    """
    return network.junctions[id]


def get_tank(network: Network, id: str) -> Tank:
    """This function returns a specific Tank from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Tank

    Returns:
      Tank with property id

    """
    return network.tanks[id]


def get_reservoir(network: Network, id: str) -> Reservoir:
    """This function returns a specific Reservoir from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Reservoir

    Returns:
      Reservoir with property id

    """
    return network.reservoirs[id]


def get_pipe(network: Network, id: str) -> Pipe:
    """This function returns a specific Pipe from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Pipe

    Returns:
      Pipe with property id

    """
    return network.pipes[id]


def get_pump(network: Network, id: str) -> Pump:
    """This function returns a specific Pump from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Pump

    Returns:
      Pump with property id

    """
    return network.pumps[id]


def get_valve(network: Network, id: str) -> Valve:
    """This function returns a specific Valve from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Valve

    Returns:
      Valve with property id

    """
    return network.valves[id]


def get_curve(network: Network, id: str) -> Curve:
    """This function returns a specific Curve from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Curve

    Returns:
      Curve with property id

    """
    return network.curves[id]


def get_pattern(network: Network, id: str) -> Pattern:
    """This function returns a specific Pattern from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Pattern

    Returns:
      Pattern with property id

    """
    return network.patterns[id]


def get_rule(network: Network, id: str) -> Rule:
    """This function returns a specific Rule from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Rule

    Returns:
      Rule with property id

    """
    return network.rules[id]


def get_node(network: Network, id: str) -> Node:
    """This function returns a specific Node from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Node

    Returns:
      Node with property id

    """
    return network.nodes[id]


def get_link(network: Network, id: str) -> Link:
    """This function returns a specific Link from the network with a specific id

    Args:
      network: OOPNET network object
      id: id of the Link

    Returns:
      Link with property id

    """
    return network.links[id]
