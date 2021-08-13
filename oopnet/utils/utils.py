import os
import numpy as np
from ..elements.network_components import Junction, Pipe
from ..report.report_getter_functions import pressure, flow


def mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        # print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)


def adddummyjunction(network, pipe, ce, dummyname='Dummy'):
    x1 = pipe.startnode.xcoordinate
    x2 = pipe.endnode.xcoordinate
    y1 = pipe.startnode.ycoordinate
    y2 = pipe.endnode.ycoordinate
    z1 = pipe.startnode.elevation
    z2 = pipe.endnode.elevation
    a = np.asarray([x1, y1, z1])
    b = np.asarray([x2, y2, z2])
    c = np.asarray(a + 0.5 * (b - a))
    n = Junction(id=dummyname,
                 xcoordinate=c[0],
                 ycoordinate=c[1],
                 elevation=c[2],
                 emittercoefficient=ce)
    # p1 = Pipe(id=pipe.id + '_a',
    #           startnode=pipe.startnode,
    #           endnode=n,
    #           length=0.5 * pipe.length,
    #           diameter=pipe.diameter,
    #           roughness=pipe.roughness,
    #           minorloss=pipe.minorloss)

    p1 = Pipe(id=pipe.id + '_a')
    p1.startnode = pipe.startnode
    p1.endnode = n
    p1.length = 0.5 * pipe.length
    p1.diameter = pipe.diameter
    p1.roughness = pipe.roughness
    p1.minorloss = pipe.minorloss

    # p2 = Pipe(id=pipe.id + '_b',
    #           startnode=n,
    #           endnode=pipe.endnode,
    #           length=0.5 * pipe.length,
    #           diameter=pipe.diameter,
    #           roughness=pipe.roughness,
    #           minorloss=pipe.minorloss)

    p2 = Pipe(id=pipe.id + '_b')
    p2.startnode = n
    p2.endnode = pipe.startnode
    p2.length = 0.5 * pipe.length
    p2.diameter = pipe.diameter
    p2.roughness = pipe.roughness
    p2.minorloss = pipe.minorloss


    pipe.status = 'CLOSED'
    network.networkhash['node'][dummyname] = n
    network.networkhash['link'][pipe.id + '_a'] = p1
    network.networkhash['link'][pipe.id + '_b'] = p2
    network.junctions.append(n)
    network.pipes.append(p1)
    network.pipes.append(p2)
    return network, p1, p2


def length(link):
    x1 = link.startnode.xcoordinate
    x2 = link.endnode.xcoordinate
    y1 = link.startnode.ycoordinate
    y2 = link.endnode.ycoordinate
    z1 = link.startnode.elevation
    z2 = link.endnode.elevation
    a = np.asarray([x1, y1, z1])
    b = np.asarray([x2, y2, z2])

    return np.linalg.norm(b - a)



def sources(network):
    """
    This function returns all sources (tanks and reservoirs) if an oopnet network
    :param network:
    :return:
    """
    if network.tanks and network.reservoirs:
        return network.reservoirs + network.tanks
    if network.tanks and not network.reservoirs:
        return network.tanks
    if not network.tanks and network.reservoirs:
        return network.reservoirs
    if not network.tanks and not network.reservoirs:
        return None


def make_measurement(report, sensors, precision=None):
    """
    This function simulates a measurement in the system at predefined sensorpositions and returns a measurement vector

    :param report: OOPNET report object
    :param sensors: dict with keys 'Flow' and/or 'Pressure' containing the node- resp. linkids as list
                    -> {'Flow':['flowsensor1', 'flowsensor2], 'Pressure':['sensor1', 'sensor2', 'sensor3']}
    :param precision: dict with keys 'Flow' and/or 'Pressure' and number of decimals -> {'Flow':3, 'Pressure':2}
    :return: numpy vector containing the measurements
    """
    vec = np.ndarray(0)
    for what in sorted(sensors.keys()):
        if what == 'Flow':
            if precision is None:
                dec = 3
            else:
                dec = precision[what]
            vec = np.around(np.concatenate((vec, flow(report)[sensors[what]].values)), decimals=dec)
        elif what == 'Pressure':
            if precision is None:
                dec = 2
            else:
                dec = precision[what]
            vec = np.around(np.concatenate((vec, pressure(report)[sensors[what]].values)), decimals=dec)
    return vec


def copy(network):
    """
    This function makes a deepcopy of an OOPNET network object

    :param network: OOPNET network object
    :return: deepcopy of OOPNET network object
    """
    return network.__deepcopy__()
