from oopnet.elements import Network, Junction, Tank, Reservoir, Pipe, Pump, Valve
from oopnet.utils.getters import get_node, get_link


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


# todo: remove Links connected to Node?
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
    network.junctions.pop(id)


def remove_reservoir(network: Network, id: str):
    """This function removes a specific Reservoir from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Reservoir ID

    """
    network.reservoirs.pop(id)


def remove_tank(network: Network, id: str):
    """This function removes a specific Tank from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Tank ID

    """
    network.tanks.pop(id)


def remove_pipe(network: Network, id: str):
    """This function removes a specific Pipe from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Pipe ID

    """
    network.pipes.pop(id)


def remove_pump(network: Network, id: str):
    """This function removes a specific Pump from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Pump ID

    """
    network.pumps.pop(id)


def remove_valve(network: Network, id: str):
    """This function removes a specific Valve from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Valve ID

    """
    network.valves.pop(id)
