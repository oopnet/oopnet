from io import TextIOWrapper

from oopnet.elements.network import Network
from oopnet.utils.getters import get_tanks, get_nodes
from oopnet.writer.decorator_writer.decorators import section_writer


@section_writer('QUALITY', 3)
def write_quality(network: Network, fid: TextIOWrapper):
    """Writes quality section to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[QUALITY]', file=fid)
    print(';id initialquality', file=fid)
    for n in get_nodes(network):
        if n.initialquality > 0.0:
            print(n.id, n.initialquality, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('REACTIONS', 3)
def write_reactions(network: Network, fid: TextIOWrapper):
    """Writes reaction settings to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[REACTIONS]', file=fid)
    r = network.reactions
    if r.orderbulk:
        print('ORDER BULK', r.orderbulk, file=fid)
    if r.orderwall:
        print('ORDER WALL', r.orderwall, file=fid)
    if r.ordertank:
        print('ORDER TANK', r.ordertank, file=fid)
    if r.globalbulk:
        print('GLOBAL BULK', r.globalbulk, file=fid)
    if r.globalwall:
        print('GLOBAL WALL', r.globalwall, file=fid)
    if r.limitingpotential:
        print('LIMITING POTENTIAL', r.limitingpotential, file=fid)
    if r.roughnesscorrelation:
        print('ROUGHNESS CORRELATION', r.roughnesscorrelation, file=fid)
    # todo: fix and enable
    # if r.bulk:
    #     for p in r.bulk:
    #         print('BULK', p.id, p.reactionbulk, file=fid)
    # if r.wall:
    #     for p in r.wall:
    #         print('WALL', p.id, p.reactionwall, file=fid)
    # if r.tank:
    #     for p in r.tank:
    #         print('TANK', p.id, p.tank, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('SOURCES', 3)
def write_sources(network: Network, fid: TextIOWrapper):
    """Writes sources section to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[SOURCES]', file=fid)
    print(';id sourcetype strength sourcepattern', file=fid)
    for n in get_nodes(network):
        if n.sourcetype:
            print(n.id, n.sourcetype, end=' ', file=fid)
            if n.strength > 0.0:
                print(n.strength, end=' ', file=fid)
            if n.sourcepattern:
                print(n.sourcepattern.id, end=' ', file=fid)
            print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('MIXING', 3)
def write_mixing(network: Network, fid: TextIOWrapper):
    """Writes mixing section to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[MIXING]', file=fid)
    print(';tankid mixingmodel compartmentvolume', file=fid)
    for t in get_tanks(network):
        if t.mixingmodel:
            print(t.id, t.mixingmodel.name, end=' ', file=fid)
            if t.compartmentvolume != 0.0:
                print(t.compartmentvolume, end=' ', file=fid)
            print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)
