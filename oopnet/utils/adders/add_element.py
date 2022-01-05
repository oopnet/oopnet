from oopnet.exceptions import ComponentExistsError
from typing import Union

from oopnet.utils.getters import get_pattern_ids, get_node_ids, get_link_ids, get_curve_ids, get_rule_ids
from oopnet.elements import Network, Junction, Reservoir, Tank, Pipe, Pump, Valve, Curve, Pattern, Node, \
    Link
from oopnet.elements.system_operation import Rule
from oopnet.elements.base import NetworkComponent


def _check_exists(obj: NetworkComponent, network: Network):
    """Checks if a component with the same ID and general type exists in the network.

    Args:
        obj: NetworkComponent that shall be added
        network: OOPNET network object

    """
    if isinstance(obj, Node):
        exists = obj.id in get_node_ids(network)
    elif isinstance(obj, Link):
        exists = obj.id in get_link_ids(network)
    elif isinstance(obj, Pattern):
        exists = obj.id in get_pattern_ids(network)
    elif isinstance(obj, Curve):
        exists = obj.id in get_curve_ids(network)
    elif isinstance(obj, Rule):
        exists = obj.id in get_rule_ids(network)
    else:
        raise TypeError(f'Trying to check the existence of an Object with an invalid type {type(obj)}.')
    if exists:
        raise ComponentExistsError(obj.id)


def _add_component(obj: NetworkComponent, component_hash: dict):
    """Adds a NetworkComponent to a hash

    Args:
        obj: NetworkComponent that shall be added
        component_hash: hash table to which the NetworkComponent shall be added

    """
    obj._component_hash = component_hash
    component_hash[obj.id] = obj


# todo: implement addition of multiple object instances?
def add_pattern(network: Network, pattern: Pattern, check_exists: bool = True):
    """Adds a Pattern to an OOPNET network object.

    Args:
      network: OOPNET network
      pattern: Pattern object to add to the network
      check_exists: if True, checks if a Pattern with the same ID already exists in the network

    """
    if check_exists:
        _check_exists(pattern, network)
    _add_component(pattern, network.patterns)


def add_curve(network: Network, curve: Curve, check_exists: bool = True):
    """Adds a Curve to an OOPNET network object.

    Args:
      network: OOPNET network object
      curve: Curve object to add to the network
      check_exists: if True, checks if a Curve with the same ID already exists in the network

    """
    if check_exists:
        _check_exists(curve, network)
    _add_component(curve, network.curves)


def add_rule(network: Network, rule: Rule, check_exists: bool = True):
    """Adds a Rule to an OOPNET network object.

    Args:
      network: OOPNET network object
      rule: Rule object to add to the network
      check_exists: if True, checks if a Rule with the same ID already exists in the network

    """
    if check_exists:
        _check_exists(rule, network)
    _add_component(rule, network.rules)


def add_junction(network: Network, junction: Junction, check_exists: bool = True):
    """Adds a Junction to an OOPNET network object.

    Args:
      network: OOPNET network object
      junction: Junction object to add to the network
      check_exists: if True, checks if a Junction with the same ID already exists in the network

    """
    if check_exists:
        _check_exists(junction, network)
    _add_component(junction, network.junctions)


def add_reservoir(network: Network, reservoir: Reservoir, check_exists: bool = True):
    """Adds a Reservoir to an OOPNET network object.

    Args:
      network: OOPNET network object
      reservoir: Reservoir object to add to the network
      check_exists: if True, checks if a Reservoir with the same ID already exists in the network

    """
    if check_exists:
        _check_exists(reservoir, network)
    _add_component(reservoir, network.reservoirs)


def add_tank(network: Network, tank: Tank, check_exists: bool = True):
    """Adds a Tank to an OOPNET network object.

    Args:
      network: OOPNET network object
      tank: Tank object to add to the network
      check_exists: if True, checks if a Tank with the same ID already exists in the network

    """
    if check_exists:
        _check_exists(tank, network)
    _add_component(tank, network.tanks)


def add_pipe(network: Network, pipe: Pipe, check_exists: bool = True):
    """Adds a Pipe to an OOPNET network object.

    Args:
      network: OOPNET network object
      pipe: Pipe object to add to the network
      check_exists: if True, checks if a Pipe with the same ID already exists in the network

    """
    if check_exists:
        _check_exists(pipe, network)
    _add_component(pipe, network.pipes)


def add_pump(network: Network, pump: Pump, check_exists: bool = True):
    """Adds a Pump to an OOPNET network object.

    Args:
      network: OOPNET network object
      pump: Pump object to add to the network
      check_exists: if True, checks if a Pump with the same ID already exists in the network

    """
    if check_exists:
        _check_exists(pump, network)
    _add_component(pump, network.pumps)


def add_valve(network: Network, valve: Valve, check_exists: bool = True):
    """Adds a Valve to an OOPNET network object.

    Args:
      network: OOPNET network object
      valve: Valve object to add to the network
      check_exists: if True, checks if a Valve with the same ID already exists in the network

    """
    if check_exists:
        _check_exists(valve, network)
    _add_component(valve, network.valves)


def add_node(network: Network, node: Union[Junction, Reservoir, Tank], check_exists: bool = True):
    """Adds a Node to an OOPNET network object.

    Args:
      network: OOPNET network object
      node: Node object to add to the network
      check_exists: if True, checks if a Node with the same ID already exists in the network

    """
    if isinstance(node, Junction):
        add_junction(network, node, check_exists=check_exists)
    elif isinstance(node, Reservoir):
        add_reservoir(network, node, check_exists=check_exists)
    elif isinstance(node, Tank):
        add_tank(network, node, check_exists=check_exists)
    else:
        raise TypeError(f'Only Node types (Junction, Tank, Reservoir) can be passed to this function but an object of '
                        f'type {type(node)} was passed.')


def add_link(network: Network, link: Union[Pipe, Pump, Valve], check_exists: bool = True):
    """Adds a Link to an OOPNET network object.

    Args:
      network: OOPNET network object
      link: Link object to add to the network
      check_exists: checks if a Link with the same ID already exists in the network

    """
    if isinstance(link, Pipe):
        add_pipe(network, link, check_exists=check_exists)
    elif isinstance(link, Pump):
        add_pump(network, link, check_exists=check_exists)
    elif isinstance(link, Valve):
        add_valve(network, link, check_exists=check_exists)
    else:
        raise TypeError(f'Only Link types (Pipe, Pump, Valve) can be passed to this function but an object of '
                        f'type {type(link)} was passed.')
