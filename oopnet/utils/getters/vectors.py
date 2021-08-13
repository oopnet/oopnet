import numpy as np
from .element_lists import get_pipes, get_junctions, get_nodes, get_tanks, get_reservoirs


def v_length(network):
    """
    Get all length values of all pipes in the network as a numpy array
    :param network: OOPNET network object
    :return: roughness as numpy.ndarray
    """
    return np.asarray([x.length for x in get_pipes(network)])


def v_diameter(network):
    """
    Get all diameter values of all pipes in the network as a numpy array
    :param network: OOPNET network object
    :return: roughness as numpy.ndarray
    """
    return np.asarray([x.diameter for x in get_pipes(network)])


def v_roughness(network):
    """
    Get all roughness values of all pipes in the network as a numpy array
    :param network: OOPNET network object
    :return: roughness as numpy.ndarray
    """
    return np.asarray([x.roughness for x in get_pipes(network)])


def v_minorloss(network):
    """
    Get all minor loss coefficient values of all pipes in the network as a numpy array
    :param network: OOPNET network object
    :return: minor loss coefficient as numpy.ndarray
    """
    return np.asarray([x.minorloss for x in get_pipes(network)])


def v_elevation(network):
    """
    Get all elevation values of all nodes in the network as a numpy array
    :param network: OOPNET network object
    :return: elevation as numpy.ndarray
    """
    return np.asarray([x.elevation for x in get_nodes(network)])


def v_emittercoefficient(network):
    """
    Get all emitter coefficients values of all junctions in the network as a numpy array
    :param network: OOPNET network object
    :return: elevation as numpy.ndarray
    """
    return np.asarray([x.emittercoefficient for x in get_junctions(network)])


def v_demand(network):
    """
    Get all emitter coefficients values of all junctions in the network as a numpy array
    :param network: OOPNET network object
    :return: demand as numpy.ndarray
    """
    return np.asarray([x.demand for x in get_junctions(network)])


def v_head(network):
    """
    Get all head values of all reservoir in the network as a numpy array
    :param network: OOPNET network object
    :return: head as numpy.ndarray
    """
    return np.asarray([x.head for x in get_reservoirs(network)])


def v_initlevel(network):
    """
    Get all initial levels of all tanks in the network as a numpy array
    :param network: OOPNET network object
    :return: initial levels as numpy.ndarray
    """
    return np.asarray([x.initlevel for x in get_tanks(network)])


def v_minlevel(network):
    """
    Get all minimum levels of all tanks in the network as a numpy array
    :param network: OOPNET network object
    :return: minimum levels as numpy.ndarray
    """
    return np.asarray([x.minlevel for x in get_tanks(network)])


def v_maxlevel(network):
    """
    Get all maximum levels of all tanks in the network as a numpy array
    :param network: OOPNET network object
    :return: maximum levels as numpy.ndarray
    """
    return np.asarray([x.maxlevel for x in get_tanks(network)])


def v_tankdiameter(network):
    """
    Get all diameters of all tanks in the network as a numpy array
    :param network: OOPNET network object
    :return: tank diameters as numpy.ndarray
    """
    return np.asarray([x.diam for x in get_tanks(network)])


def v_minvolume(network):
    """
    Get all minimal volumes of all tanks in the network as a numpy array
    :param network: OOPNET network object
    :return: minimal volumes as numpy.ndarray
    """
    return np.asarray([x.minvolume for x in get_tanks(network)])

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