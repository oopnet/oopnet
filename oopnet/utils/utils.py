from __future__ import annotations
import os
from typing import Optional, TYPE_CHECKING
from copy import deepcopy

import numpy as np

if TYPE_CHECKING:
    from oopnet.elements.network_components import Junction, Pipe
from oopnet.report import Pressure, Flow
from oopnet.report.xrayreport import Report


def mkdir(newdir: str):
    """Creates a new directory.

    - already exists, silently complete
    - regular file in the way, raise an exception
    - parent directory(ies) does not exist, make them as well

    Args:
      newdir: path to be created

    Returns:

    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        if tail:
            os.mkdir(newdir)


# todo: remove?
def adddummyjunction(network, pipe, ce, dummyname='Dummy'):
    """

    Args:
      network: 
      pipe: 
      ce: 
      dummyname:  (Default value = 'Dummy')

    Returns:

    """
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
    network._junctions.append(n)
    network._pipes.append(p1)
    network._pipes.append(p2)
    return network, p1, p2


def length(link):
    """

    Args:
      link: 

    Returns:

    """
    x1 = link.startnode.xcoordinate
    x2 = link.endnode.xcoordinate
    y1 = link.startnode.ycoordinate
    y2 = link.endnode.ycoordinate
    z1 = link.startnode.elevation
    z2 = link.endnode.elevation
    a = np.asarray([x1, y1, z1])
    b = np.asarray([x2, y2, z2])

    return np.linalg.norm(b - a)


# todo: check if functionality exists elsewhere; check for nodes with negative demands?
def sources(network):
    """This function returns all sources (tanks and reservoirs) if an oopnet network

    Args:
      network: return:

    Returns:

    """
    if network._tanks and network._reservoirs:
        return network._reservoirs + network._tanks
    if network._tanks:
        return network._tanks
    if network._reservoirs:
        return network._reservoirs
    return None


def make_measurement(report: Report, sensors: dict, precision: Optional[dict] = None):
    """This function simulates a measurement in the system at predefined sensorpositions and returns a measurement vector

    Args:
      report: OOPNET report object
      sensors: dict with keys 'Flow' and/or 'Pressure' containing the node- resp. linkids as list
    -> {'Flow':['flowsensor1', 'flowsensor2], 'Pressure':['sensor1', 'sensor2', 'sensor3']}
      precision: dict with keys 'Flow' and/or 'Pressure' and number of decimals -> {'Flow':3, 'Pressure':2}
      report: Report: 
      sensors: dict: 
      precision: Optional[dict]:  (Default value = None)

    Returns:
      numpy vector containing the measurements

    """
    vec = np.ndarray(0)
    for what in sorted(sensors.keys()):
        if what == 'Flow':
            dec = 3 if precision is None else precision[what]
            vec = np.around(np.concatenate((vec, Flow(report)[sensors[what]].values)), decimals=dec)
        elif what == 'Pressure':
            dec = 2 if precision is None else precision[what]
            vec = np.around(np.concatenate((vec, Pressure(report)[sensors[what]].values)), decimals=dec)
    return vec


def copy(network):
    """This function makes a deepcopy of an OOPNET network object

    Args:
      network: OOPNET network object

    Returns:
      deepcopy of OOPNET network object

    """
    return deepcopy(network)
