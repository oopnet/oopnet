from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from oopnet.utils.getters.get_by_id import get_node, get_link, get_pattern
from oopnet.reader.decorators import section_reader
if TYPE_CHECKING:
    from oopnet.elements.network import Network


logger = logging.getLogger(__name__)


@section_reader('QUALITY', 3)
def read_quality(network: Network, block: list):
    """Reads quality settings from block.

    Args:
      network: OOPNET network object where the quality settings shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading quality section')
    for vals in block:
        vals = vals['values']
        j = get_node(network, vals[0])
        if len(vals) > 1:
            j.initialquality = float(vals[1])


@section_reader('REACTIONS', 3)
def read_reaction(network: Network, block: list):
    """Reads reaction settings from block.

    Args:
      network: OOPNET network object where the reaction settings shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading reactions')
    r = network.reactions
    for vals in block:
        vals = vals['values']
        vals[0] = vals[0].upper()
        if vals[0] == 'ORDER':
            vals[1] = vals[1].upper()
            if vals[1] == 'BULK':
                r.orderbulk = float(vals[2])
            elif vals[1] == 'WALL':
                r.orderwall = float(vals[2])
            elif vals[1] == 'TANK':
                r.ordertank = float(vals[2])
        elif vals[0] == 'GLOBAL':
            vals[1] = vals[1].upper()
            if vals[1] == 'BULK':
                r.globalbulk = float(vals[2])
            elif vals[1] == 'WALL':
                r.globalwall = float(vals[2])
        elif vals[0] == 'LIMITING' and vals[1].upper() == 'POTENTIAL':
            r.limitingpotential = float(vals[2])
        elif vals[0] == 'ROUGHNESS' and vals[1].upper() == 'CORRELATION':
            r.roughnesscorrelation = float(vals[2])
        elif vals[0] == 'BULK':
            p = get_link(network, vals[1])
            p.reactionbulk = float(vals[2])
            if r.bulk is None:
                r.bulk = [p]
            else:
                r.bulk.append(p)
        elif vals[0] == 'WALL':
            p = get_link(network, vals[1])
            p.reactionwall = float(vals[2])
            if r.wall is None:
                r.wall = [p]
            else:
                r.wall.append(p)
        elif vals[0] == 'TANK':
            p = get_link(network, vals[1])
            p.reactiontank = float(vals[2])
            if r.tank is None:
                r.tank = [p]
            else:
                r.tank.append(p)


@section_reader('SOURCES', 3)
def read_sources(network: Network, block: list):
    """Reads sources from block.

    Args:
      network: OOPNET network object where the sources shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading sources section')
    for vals in block:
        vals = vals['values']
        n = get_node(network, vals[0])
        if len(vals) > 1:
            n.sourcetype = vals[1].upper()
        if len(vals) > 2:
            n.strength = float(vals[2])
        if len(vals) > 3:
            n.sourcepattern = get_pattern(network, vals[3])


@section_reader('MIXING', 3)
def read_mixing(network: Network, block: list):
    """Reads mixing settings from block.

    Args:
      network: OOPNET network object where the mixing settings shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading mixing section')
    for vals in block:
        vals = vals['values']
        t = get_node(network, vals[0])
        if len(vals) > 1:
            t.mixingmodel = vals[1].upper()
        if len(vals) > 2:
            t.compartmentvolume = float(vals[2])
