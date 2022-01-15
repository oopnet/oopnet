from oopnet.elements import Network, Pipe, Junction, Reservoir, Tank, Node, Link, Pump, Valve, Curve, Pattern, Energy, \
    Control, Rule


def get_pattern_ids(network: Network) -> list[str]:
    """Gets all Pattern IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Pattern IDs

    """
    return list(network.patterns.keys())


def get_curve_ids(network: Network) -> list[str]:
    """Gets all Curve IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Curve IDs

    """
    return list(network.curves.keys())


def get_rule_ids(network: Network) -> list[str]:
    """Gets all Rule IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Rule IDs

    """
    return list(network.rules.keys())


def get_junction_ids(network: Network) -> list[str]:
    """Gets all Junction IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Junction IDs

    """
    return list(network.junctions.keys())


def get_tank_ids(network: Network) -> list[str]:
    """Gets all Tank IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Tank IDs

    """
    return list(network.tanks.keys())


def get_reservoir_ids(network: Network) -> list[str]:
    """Gets all Reservoir IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Reservoir IDs

    """
    return list(network.reservoirs.keys())


def get_node_ids(network: Network) -> list[str]:
    """Gets all Node IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Node IDs

    """
    return get_junction_ids(network) + get_tank_ids(network) + get_reservoir_ids(network)


def get_pipe_ids(network: Network) -> list[str]:
    """Gets all Pipe IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Pipe IDs

    """
    return list(network.pipes.keys())


def get_pump_ids(network: Network) -> list[str]:
    """Gets all Pump IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Pump IDs

    """
    return list(network.pumps.keys())


def get_valve_ids(network: Network) -> list[str]:
    """Gets all Valve IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Valve IDs

    """
    return list(network.valves.keys())


def get_link_ids(network: Network) -> list[str]:
    """Gets all Link IDs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Link IDs

    """
    return get_pipe_ids(network) + get_pump_ids(network) + get_valve_ids(network)


# Retrieve all specific objects
def get_pipes(network: Network) -> list[Pipe]:
    """Gets all Pipes in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Pipes

    """
    return list(network.pipes.values())


def get_junctions(network: Network) -> list[Junction]:
    """Gets all Junctions in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Junctions

    """
    return list(network.junctions.values())


def get_reservoirs(network: Network) -> list[Reservoir]:
    """Gets all Reservoirs in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Reservoirs

    """
    return list(network.reservoirs.values())


def get_tanks(network: Network) -> list[Tank]:
    """Gets all Tanks in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Tanks

    """
    return list(network.tanks.values())


def get_nodes(network: Network) -> list[Node]:
    """Gets all Nodes (Junctions, Reservoirs and Tanks) in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Nodes

    """
    return get_junctions(network) + get_tanks(network) + get_reservoirs(network)


def get_links(network: Network) -> list[Link]:
    """Gets all Links (Pipes, Pumps and Valves) in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Links

    """
    return get_pipes(network) + get_pumps(network) + get_valves(network)


def get_pumps(network: Network) -> list[Pump]:
    """Gets all Pumps in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Pumps

    """
    return list(network.pumps.values())


def get_valves(network: Network) -> list[Valve]:
    """Gets all Valves in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Valves

    """
    return list(network.valves.values())


def get_curves(network: Network) -> list[Curve]:
    """Gets all Curves in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Curves

    """
    return list(network.curves.values())


def get_patterns(network: Network) -> list[Pattern]:
    """Gets all Patterns in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Patterns

    """
    return list(network.patterns.values())


def get_energies(network: Network) -> list[Energy]:
    """Gets all Energy entries in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Energy entries

    """
    return network.energies


def get_controls(network: Network) -> list[Control]:
    """Gets all Controls in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Controls

    """
    return network.controls


def get_rules(network: Network) -> list[Rule]:
    """Gets all Rules in a network.

    Args:
      network: OOPNET network object

    Returns:
      list of Rules

    """
    return list(network.rules.values())
