from __future__ import annotations
from typing import TYPE_CHECKING
from io import TextIOWrapper
import logging

from oopnet.utils.getters.element_lists import get_tanks, get_nodes
from oopnet.writer.decorators import section_writer
if TYPE_CHECKING:
    from oopnet.elements.network import Network

logger = logging.getLogger(__name__)


@section_writer('QUALITY', 3)
def write_quality(network: Network, fid: TextIOWrapper):
    """Writes quality section to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Quality section')
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
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Reactions section')
    print('[REACTIONS]', file=fid)
    r = network.reactions
    print('ORDER BULK', r.orderbulk, file=fid)
    print('ORDER WALL', r.orderwall, file=fid)
    print('ORDER TANK', r.ordertank, file=fid)
    print('GLOBAL BULK', r.globalbulk, file=fid)
    print('GLOBAL WALL', r.globalwall, file=fid)
    if r.limitingpotential is not None:
        print('LIMITING POTENTIAL', r.limitingpotential, file=fid)
    if r.roughnesscorrelation is not None:
        print('ROUGHNESS CORRELATION', r.roughnesscorrelation, file=fid)
    if r.bulk:
        for p in r.bulk:
            print('BULK', p.id, p.reactionbulk, file=fid)
    if r.wall:
        for p in r.wall:
            print('WALL', p.id, p.reactionwall, file=fid)
    if r.tank:
        for p in r.tank:
            print('TANK', p.id, p.tank, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('SOURCES', 3)
def write_sources(network: Network, fid: TextIOWrapper):
    """Writes sources section to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Sources section')
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
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Mixing section')
    print('[MIXING]', file=fid)
    print(';tankid mixingmodel compartmentvolume', file=fid)
    for t in get_tanks(network):
        if t.mixingmodel:
            print(t.id, t.mixingmodel, end=' ', file=fid)
            if t.compartmentvolume and t.compartmentvolume != 0.0:
                print(t.compartmentvolume, end=' ', file=fid)
            print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)
