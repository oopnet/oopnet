from oopnet.utils.getters.get_by_id import *
from oopnet.elements.network_components import *


def remove_link(network, lid):
    '''
    This function removes a specific Link from an OOPNET network

    :param network: OOPNET network object
    :param lid: Link ID
    '''
    l = get_link(network, lid)
    if isinstance(l, Pipe):
        remove_pipe(network, lid)
    elif isinstance(l, Pump):
        remove_pump(network, lid)
    elif isinstance(l, Valve):
        remove_valve(network, lid)
    else:
        raise Exception(f'No link with ID {lid} in the network.')


def remove_node(network, nid):
    '''
    This function removes a specific Node from an OOPNET network

    :param network: OOPNET network object
    :param nid: Node ID
    '''
    n = get_node(network, nid)
    if isinstance(n, Junction):
        remove_junction(network, nid)
    elif isinstance(n, Tank):
        remove_tank(network, nid)
    elif isinstance(n, Reservoir):
        remove_reservoir(network, nid)
    else:
        raise Exception(f'No node with ID {nid} in the network.')


def remove_junction(network, id):
    '''
    This function removes a specific Junction from an OOPNET network.

    :param network: OOPNET network object
    :param id: Junction ID
    '''
    j = get_junction(network, id)
    network.junctions.remove(j)
    del network.networkhash['node'][id]


def remove_reservoir(network, id):
    '''
    This function removes a specific Reservoir from an OOPNET network.

    :param network: OOPNET network object
    :param id: Reservoir ID
    '''
    r = get_reservoir(network, id)
    network.reservoirs.remove(r)
    del network.networkhash['node'][id]


def remove_tank(network, id):
    '''
    This function removes a specific Tank from an OOPNET network.

    :param network: OOPNET network object
    :param id: Tank ID
    '''
    t = get_tank(network, id)
    network.tanks.remove(t)
    del network.networkhash['node'][id]


def remove_pipe(network, id):
    '''
    This function removes a specific Pipe from an OOPNET network.

    :param network: OOPNET network object
    :param id: Pipe ID

    '''
    p = get_pipe(network, id)
    network.pipes.remove(p)
    del network.networkhash['link'][id]


def remove_pump(network, id):
    '''
    This function removes a specific Pump from an OOPNET network.

    :param network: OOPNET network object
    :param id: Pump ID
    '''
    p = get_pump(network, id)
    network.pumps.remove(p)
    del network.networkhash['link'][id]


def remove_valve(network, id):
    '''
    This function removes a specific Valve from an OOPNET network.

    :param network: OOPNET network object
    :param id: Valve ID
    '''
    v = get_valve(network, id)
    network.valves.remove(v)
    del network.networkhash['link'][id]
