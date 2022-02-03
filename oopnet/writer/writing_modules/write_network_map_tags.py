from __future__ import annotations
from typing import TYPE_CHECKING
from io import TextIOWrapper
import logging

from oopnet.utils.getters.element_lists import get_nodes, get_links
from oopnet.writer.decorators import section_writer
if TYPE_CHECKING:
    from oopnet.elements.network import Network

logger = logging.getLogger(__name__)


@section_writer('COORDINATES', 4)
def write_coordinates(network: Network, fid: TextIOWrapper):
    """Writes coordinates to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Coordinates section')
    print('[COORDINATES]', file=fid)
    print(';nodeid xcoordinate ycoordinate', file=fid)
    for n in get_nodes(network):
        print(n.id, n.xcoordinate, n.ycoordinate, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('VERTICES', 4)
def write_vertices(network: Network, fid: TextIOWrapper):
    """Writes vertices to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Vertices section')
    print('[VERTICES]', file=fid)
    print(';linkkid xcoordinate ycoordinate', file=fid)
    for l in get_links(network):
        for v in l.vertices:
            print(l.id, v.xcoordinate, v.ycoordinate, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('LABELS', 4)
def write_labels(network: Network, fid: TextIOWrapper):
    """Writes labels to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    # ToDo: Implement Printer for Labels
    # logger.debug('Writing Labels section')
    print('[LABELS]', file=fid)
    print(';xcoordinate ycoordinate label anchornode', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('BACKDROP', 4)
def write_backdrop(network: Network, fid: TextIOWrapper):
    """Writes backdrop data to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    # ToDo: Implement Printer for Backdrop
    # logger.debug('Writing Backdrop section')
    print('[BACKDROP]', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('TAGS', 4)
def write_tags(network: Network, fid: TextIOWrapper):
    """Writes tags to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    # ToDo: Implement Printer for Tags
    # logger.debug('Writing Tags section')
    print('[TAGS]', file=fid)
    print('\n', end=' ', file=fid)
