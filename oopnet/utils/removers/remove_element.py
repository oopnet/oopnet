from oopnet.utils.getters.get_by_id import *


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
