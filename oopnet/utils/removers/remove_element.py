from oopnet.elements.network import Network
from oopnet.utils.getters.get_by_id import get_node, get_link, get_junction, get_reservoir, get_tank, get_pipe, \
    get_pump, get_valve
from oopnet.elements.network_components import Junction, Tank, Reservoir, Pipe, Pump, Valve


def remove_link(network: Network, id: str):
    """This function removes a specific Link from an OOPNET network

    Args:
      network: OOPNET network object
      id: Link ID

    """
    l = get_link(network, id)
    if isinstance(l, Pipe):
        remove_pipe(network, id)
    elif isinstance(l, Pump):
        remove_pump(network, id)
    elif isinstance(l, Valve):
        remove_valve(network, id)
    else:
        raise Exception(f'No link with ID {id} in the network.')


def remove_node(network: Network, id: str):
    """This function removes a specific Node from an OOPNET network

    Args:
      network: OOPNET network object
      id: Node ID

    """
    n = get_node(network, id)
    if isinstance(n, Junction):
        remove_junction(network, id)
    elif isinstance(n, Tank):
        remove_tank(network, id)
    elif isinstance(n, Reservoir):
        remove_reservoir(network, id)
    else:
        raise Exception(f'No node with ID {id} in the network.')


def remove_junction(network: Network, id: str):
    """This function removes a specific Junction from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Junction ID

    """
    j = get_junction(network, id)
    network.junctions.remove(j)


def remove_reservoir(network: Network, id: str):
    """This function removes a specific Reservoir from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Reservoir ID

    """
    r = get_reservoir(network, id)
    network.reservoirs.remove(r)


def remove_tank(network: Network, id: str):
    """This function removes a specific Tank from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Tank ID

    """
    t = get_tank(network, id)
    network.tanks.remove(t)


def remove_pipe(network: Network, id: str):
    """This function removes a specific Pipe from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Pipe ID

    """
    p = get_pipe(network, id)
    network.pipes.remove(p)


def remove_pump(network: Network, id: str):
    """This function removes a specific Pump from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Pump ID

    """
    p = get_pump(network, id)
    network.pumps.remove(p)


def remove_valve(network: Network, id: str):
    """This function removes a specific Valve from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Valve ID

    """
    v = get_valve(network, id)
    network.valves.remove(v)
