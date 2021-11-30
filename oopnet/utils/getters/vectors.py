import numpy as np

from oopnet.elements.network import Network
from oopnet.utils.getters.element_lists import get_pipes, get_junctions, get_nodes, get_tanks, get_reservoirs


def v_length(network: Network) -> np.array:
    """Get all length values of all pipes in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      roughness as numpy.ndarray

    """
    return np.asarray([x.length for x in get_pipes(network)])


# todo: make v_diameter return valve diameters?
def v_diameter(network: Network) -> np.array:
    """Get all diameter values of all pipes in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      roughness as numpy.ndarray

    """
    return np.asarray([x.diameter for x in get_pipes(network)])


def v_roughness(network: Network) -> np.array:
    """Get all roughness values of all pipes in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      roughness as numpy.ndarray

    """
    return np.asarray([x.roughness for x in get_pipes(network)])


def v_minorloss(network: Network) -> np.array:
    """Get all minor loss coefficient values of all pipes in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      minor loss coefficient as numpy.ndarray

    """
    return np.asarray([x.minorloss for x in get_pipes(network)])


def v_elevation(network: Network) -> np.array:
    """Get all elevation values of all nodes in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      elevation as numpy.ndarray

    """
    return np.asarray([x.elevation for x in get_nodes(network)])


def v_emittercoefficient(network: Network) -> np.array:
    """Get all emitter coefficients values of all junctions in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      elevation as numpy.ndarray

    """
    return np.asarray([x.emittercoefficient for x in get_junctions(network)])


def v_demand(network: Network) -> np.array:
    """Get all emitter coefficients values of all junctions in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      demand as numpy.ndarray

    """
    return np.asarray([x.demand for x in get_junctions(network)])


def v_head(network: Network) -> np.array:
    """Get all head values of all reservoir in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      head as numpy.ndarray

    """
    return np.asarray([x.head for x in get_reservoirs(network)])


def v_initlevel(network: Network) -> np.array:
    """Get all initial levels of all tanks in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      initial levels as numpy.ndarray

    """
    return np.asarray([x.initlevel for x in get_tanks(network)])


def v_minlevel(network: Network) -> np.array:
    """Get all minimum levels of all tanks in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      minimum levels as numpy.ndarray

    """
    return np.asarray([x.minlevel for x in get_tanks(network)])


def v_maxlevel(network: Network) -> np.array:
    """Get all maximum levels of all tanks in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      maximum levels as numpy.ndarray

    """
    return np.asarray([x.maxlevel for x in get_tanks(network)])


def v_tankdiameter(network: Network) -> np.array:
    """Get all diameters of all tanks in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      tank diameters as numpy.ndarray

    """
    return np.asarray([x.diam for x in get_tanks(network)])


def v_minvolume(network: Network) -> np.array:
    """Get all minimal volumes of all tanks in the network as a numpy array

    Args:
      network: OOPNET network object

    Returns:
      minimal volumes as numpy.ndarray

    """
    return np.asarray([x.minvolume for x in get_tanks(network)])

# todo: remove
# if __name__ == '__main__':
#
#
#     from oopnet.api import *
#
#     filename = os.path.join('..', '..', '..', 'examples', 'data', 'Poulakis.inp')
#     net = Read(filename)
#
#
#     print net.options.units
#
#     r = v_roughness(net)
#     print r, type(r), r.shape
#
#     d = v_diameter(net)
#     print d, type(d), d.shape
#
#     d = v_length(net)
#     print d, type(d), d.shape
#
#     d = v_minorloss(net)
#     print d, type(d), d.shape
#
#     d = v_elevation(net)
#     print d, type(d), d.shape
#
#     print 'Emitter'
#     d = v_emittercoefficient(net)
#     print d, type(d), d.shape
#
#     print 'Demand'
#     d = v_demand(net)
#     print d, type(d), d.shape
#
#     print 'Head'
#     d = v_head(net)
#     print d, type(d), d.shape
#
#     print 'Initial Level'
#     d = v_initlevel(net)
#     print d, type(d), d.shape
#
#     print 'Min Level'
#     d = v_minlevel(net)
#     print d, type(d), d.shape
#
#     print 'Max Level'
#     d = v_maxlevel(net)
#     print d, type(d), d.shape
#
#     print 'Tank diameter'
#     d = v_tankdiameter(net)
#     print d, type(d), d.shape
#
#     print 'Minimal Volume'
#     d = v_minvolume(net)
#     print d, type(d), d.shape