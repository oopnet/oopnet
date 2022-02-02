from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from oopnet.elements.network import Network
    from oopnet.elements.network_components import Pipe, Junction, Reservoir, Tank, Node, Link, Pump, Valve, Curve, \
        Pattern
    from oopnet.elements.system_operation import Rule


def get_junction(network: Network, id: str) -> Junction:
    """Gets a specific Junction from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Junction

    Returns:
      Junction with property ID

    """
    return network._nodes['junctions'][id]


def get_tank(network: Network, id: str) -> Tank:
    """Gets a specific Tank from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Tank

    Returns:
      Tank with property ID

    """
    return network._nodes['tanks'][id]


def get_reservoir(network: Network, id: str) -> Reservoir:
    """Gets a specific Reservoir from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Reservoir

    Returns:
      Reservoir with property ID

    """
    return network._nodes['reservoirs'][id]


def get_pipe(network: Network, id: str) -> Pipe:
    """Gets a specific Pipe from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Pipe

    Returns:
      Pipe with property ID

    """
    return network._links['pipes'][id]


def get_pump(network: Network, id: str) -> Pump:
    """Gets a specific Pump from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Pump

    Returns:
      Pump with property ID

    """
    return network._links['pumps'][id]


def get_valve(network: Network, id: str) -> Valve:
    """Gets a specific Valve from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Valve

    Returns:
      Valve with property ID

    """
    return network._links['valves'][id]


def get_curve(network: Network, id: str) -> Curve:
    """Gets a specific Curve from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Curve

    Returns:
      Curve with property ID

    """
    return network._curves[id]


def get_pattern(network: Network, id: str) -> Pattern:
    """Gets a specific Pattern from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Pattern

    Returns:
      Pattern with property ID

    """
    return network._patterns[id]


def get_rule(network: Network, id: str) -> Rule:
    """Gets a specific Rule from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Rule

    Returns:
      Rule with property ID

    """
    return network._rules[id]


def get_node(network: Network, id: str) -> Node:
    """Gets a specific Node from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Node

    Returns:
      Node with property ID

    """
    for vals in network._nodes.values():
        if id in vals:
            return vals[id]


def get_link(network: Network, id: str) -> Link:
    """Gets a specific Link from the network with a specific ID.

    Args:
      network: OOPNET network object
      id: ID of the Link

    Returns:
      Link with property ID

    """
    for vals in network._links.values():
        if id in vals:
            return vals[id]
