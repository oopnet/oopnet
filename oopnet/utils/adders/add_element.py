from __future__ import annotations
from typing import Union, TYPE_CHECKING
import logging

from oopnet.utils.oopnet_logging import logging_decorator
from oopnet.elements.network_components import Junction, Reservoir, Tank, Pipe, Pump, Valve
from oopnet.elements.system_operation import Curve, Pattern
if TYPE_CHECKING:
    from oopnet.elements.system_operation import Rule
    from oopnet.elements.base import NetworkComponent
    from oopnet.elements.network import Network

logger = logging.getLogger(__name__)


@logging_decorator(logger)
def _add_component(obj: Union[NetworkComponent, Rule], network: Network, component_hash: dict):
    """Adds a NetworkComponent to a registry.

    Args:
        obj: NetworkComponent that shall be added
        network: Network to which the NetworkComponent is added
        component_hash: hash table to which the NetworkComponent is added

    """
    obj._network = network
    component_hash[obj.id] = obj


def add_pattern(network: Network, pattern: Pattern):
    """Adds a Pattern to an OOPNET network object.

    Args:
      network: OOPNET network
      pattern: Pattern object to add to the network

    """
    _add_component(pattern, network, network._patterns)


def add_curve(network: Network, curve: Curve):
    """Adds a Curve to an OOPNET network object.

    Args:
      network: OOPNET network object
      curve: Curve object to add to the network

    """
    _add_component(curve, network, network._curves)


def add_rule(network: Network, rule: Rule):
    """Adds a Rule to an OOPNET network object.

    Args:
      network: OOPNET network object
      rule: Rule object to add to the network

    """
    _add_component(rule, network, network._rules)


def add_junction(network: Network, junction: Junction):
    """Adds a Junction to an OOPNET network object.

    Args:
      network: OOPNET network object
      junction: Junction object to add to the network

    """
    _add_component(junction, network, network._nodes['junctions'])


def add_reservoir(network: Network, reservoir: Reservoir):
    """Adds a Reservoir to an OOPNET network object.

    Args:
      network: OOPNET network object
      reservoir: Reservoir object to add to the network

    """
    _add_component(reservoir, network, network._nodes['reservoirs'])


def add_tank(network: Network, tank: Tank):
    """Adds a Tank to an OOPNET network object.

    Args:
      network: OOPNET network object
      tank: Tank object to add to the network

    """
    _add_component(tank, network, network._nodes['tanks'])


def add_pipe(network: Network, pipe: Pipe):
    """Adds a Pipe to an OOPNET network object.

    Args:
      network: OOPNET network object
      pipe: Pipe object to add to the network

    """
    _add_component(pipe, network, network._links['pipes'])


def add_pump(network: Network, pump: Pump):
    """Adds a Pump to an OOPNET network object.

    Args:
      network: OOPNET network object
      pump: Pump object to add to the network

    """
    _add_component(pump, network, network._links['pumps'])


def add_valve(network: Network, valve: Valve):
    """Adds a Valve to an OOPNET network object.

    Args:
      network: OOPNET network object
      valve: Valve object to add to the network

    """
    _add_component(valve, network, network._links['valves'])


def add_node(network: Network, node: Union[Junction, Reservoir, Tank]):
    """Adds a Node to an OOPNET network object.

    Args:
      network: OOPNET network object
      node: Node object to add to the network

    """
    if isinstance(node, Junction):
        add_junction(network, node)
    elif isinstance(node, Reservoir):
        add_reservoir(network, node)
    elif isinstance(node, Tank):
        add_tank(network, node)
    else:
        raise TypeError(f'Only Node types (Junction, Tank, Reservoir) can be passed to this function but an object of '
                        f'type {type(node)} was passed.')


def add_link(network: Network, link: Union[Pipe, Pump, Valve]):
    """Adds a Link to an OOPNET network object.

    Args:
      network: OOPNET network object
      link: Link object to add to the network

    """
    if isinstance(link, Pipe):
        add_pipe(network, link)
    elif isinstance(link, Pump):
        add_pump(network, link)
    elif isinstance(link, Valve):
        add_valve(network, link)
    else:
        raise TypeError(f'Only Link types (Pipe, Pump, Valve) can be passed to this function but an object of '
                        f'type {type(link)} was passed.')
