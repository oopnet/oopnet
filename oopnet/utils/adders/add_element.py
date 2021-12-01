from typing import Optional, Union

from oopnet.elements.base import NetworkComponent
from oopnet.utils.getters.element_lists import get_pattern_ids, get_node_ids, get_link_ids, get_curve_ids
from oopnet.elements.network import Network
from oopnet.elements.network_components import Junction, Reservoir, Tank, Pipe, Pump, Valve, Curve, Pattern, Node, Link


class ComponentExistsException(Exception):
    """ """
    def __init__(self, id, message=None):
        if not message:
            self.message = f'A component with the ID "{id}" already exists in the network.'
        super().__init__(self.message)


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
    else:
        raise TypeError(f'Trying to check the existence of an Object with an invalid type {type(obj)}.')
    if exists:
        raise ComponentExistsException(obj.id)


def _add_component(obj: NetworkComponent, component_hash: dict):
    """Adds a NetworkComponent to a hash

    Args:
        obj: NetworkComponent that shall be added
        component_hash: hash table to which the NetworkComponent shall be added

    """
    obj._component_hash = component_hash
    component_hash[obj.id] = obj


# todo: implement addition of multiple object instances?
def add_pattern(network: Network, pattern: Optional[Pattern] = None, check_exists: bool = True, **kwargs):
    """Adds a Pattern to an OOPNET network object.
    
    This function takes either a Pattern object OR the keyword arguments to initialize a new Pattern object.

    Args:
      network: OOPNET network
      pattern: Pattern object to add to the network
      check_exists: if True, checks if a Pattern with the same ID already exists in the network
      **kwargs: Pattern init keyword arguments

    """
    if not pattern:
        pattern = Pattern(**kwargs)
    if check_exists:
        _check_exists(pattern, network)
    _add_component(pattern, network.patterns)


def add_curve(network: Network, curve: Optional[Curve] = None, check_exists: bool = True, **kwargs):
    """Adds a Curve to an OOPNET network object.
    
    This function takes either a Curve object OR the keyword arguments to initialize a new Curve object.

    Args:
      network: OOPNET network object
      curve: Curve object to add to the network
      check_exists: if True, checks if a Curve with the same ID already exists in the network
      **kwargs: Curve init keyword arguments

    """
    if not curve:
        curve = Curve(**kwargs)
    if check_exists:
        _check_exists(curve, network)
    _add_component(curve, network.curves)


def add_junction(network: Network, junction: Optional[Junction] = None, check_exists: bool = True, **kwargs):
    """Adds a Junction to an OOPNET network object.
    
    This function takes either a Junction object OR the keyword arguments to initialize a new Junction object.

    Args:
      network: OOPNET network object
      junction: Junction object to add to the network
      check_exists: if True, checks if a Junction with the same ID already exists in the network
      **kwargs: Junction init keyword arguments

    """
    if not junction:
        junction = Junction(**kwargs)
    if check_exists:
        _check_exists(junction, network)
    _add_component(junction, network.junctions)


def add_reservoir(network: Network, reservoir: Optional[Reservoir] = None, check_exists: bool = True, **kwargs):
    """Adds a Reservoir to an OOPNET network object.
    
    This function takes either a Reservoir object OR the keyword arguments to initialize a new Reservoir object.

    Args:
      network: OOPNET network object
      reservoir: Reservoir object to add to the network
      check_exists: if True, checks if a Reservoir with the same ID already exists in the network
      **kwargs: Reservoir init keyword arguments

    """
    if not reservoir:
        reservoir = Reservoir(**kwargs)
    if check_exists:
        _check_exists(reservoir, network)
    _add_component(reservoir, network.reservoirs)


def add_tank(network: Network, tank: Optional[Tank] = None, check_exists: bool = True, **kwargs):
    """Adds a Tank to an OOPNET network object.
    
    This function takes either a Tank object OR the keyword arguments to initialize a new Tank object.

    Args:
      network: OOPNET network object
      tank: Tank object to add to the network
      check_exists: if True, checks if a Tank with the same ID already exists in the network
      **kwargs: Tank init keyword arguments

    """
    if not tank:
        tank = Tank(**kwargs)
    if check_exists:
        _check_exists(tank, network)
    _add_component(tank, network.tanks)


def add_pipe(network: Network, pipe: Optional[Pipe] = None, check_exists: bool = True, **kwargs):
    """Adds a Pipe to an OOPNET network object.
    
    This function takes either a Pipe object OR the keyword arguments to initialize a new Pipe object.

    Args:
      network: OOPNET network object
      pipe: Pipe object to add to the network
      check_exists: if True, checks if a Pipe with the same ID already exists in the network
      **kwargs: Pipe init keyword arguments

    """
    if not pipe:
        pipe = Pipe(**kwargs)
    if check_exists:
        _check_exists(pipe, network)
    _add_component(pipe, network.pipes)


def add_pump(network: Network, pump: Optional[Pump] = None, check_exists: bool = True, **kwargs):
    """Adds a Pump to an OOPNET network object.
    
    This function takes either a Pump object OR the keyword arguments to initialize a new Pump object.

    Args:
      network: OOPNET network object
      pump: Pump object to add to the network
      check_exists: if True, checks if a Pump with the same ID already exists in the network
      **kwargs: Pump init keyword arguments

    """
    if not pump:
        pump = Pump(**kwargs)
    if check_exists:
        _check_exists(pump, network)
    _add_component(pump, network.pumps)


def add_valve(network: Network, valve: Optional[Valve] = None, check_exists: bool = True, **kwargs):
    """Adds a Valve to an OOPNET network object.
    
    This function takes either a Valve object OR the keyword arguments to initialize a new Valve object.

    Args:
      network: OOPNET network object
      valve: Valve object to add to the network
      check_exists: if True, checks if a Valve with the same ID already exists in the network
      **kwargs: Valve init keyword arguments

    """
    if not valve:
        valve = Valve(**kwargs)
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
