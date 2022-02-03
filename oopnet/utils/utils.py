from __future__ import annotations
import os
from typing import Optional, TYPE_CHECKING
from copy import deepcopy

import numpy as np

if TYPE_CHECKING:
    from oopnet.elements.network_components import Junction, Pipe
from oopnet.report.report import Report


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
            vec = np.around(np.concatenate((vec, report.flow[sensors[what]].values)), decimals=dec)
        elif what == 'Pressure':
            dec = 2 if precision is None else precision[what]
            vec = np.around(np.concatenate((vec, report.pressure[sensors[what]].values)), decimals=dec)
    return vec


def copy(network):
    """This function makes a deepcopy of an OOPNET network object

    Args:
      network: OOPNET network object

    Returns:
      deepcopy of OOPNET network object

    """
    return deepcopy(network)
