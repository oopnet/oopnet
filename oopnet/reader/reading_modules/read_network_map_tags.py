from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from oopnet.utils.getters import get_link

from oopnet.utils.getters.get_by_id import get_node
from oopnet.reader.decorators import section_reader
from oopnet.elements.network_map_tags import Vertex
if TYPE_CHECKING:
    from oopnet.elements.network import Network


logger = logging.getLogger(__name__)


@section_reader('COORDINATES', 4)
def read_coordinates(network: Network, block: list):
    """Reads coordinates from block.

    Args:
      network: OOPNET network object where the coordinates shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading Coordinates section')
    for vals in block:
        vals = vals['values']
        j = get_node(network, vals[0])
        if len(vals) > 1:
            j.xcoordinate = float(vals[1])
        if len(vals) > 2:
            j.ycoordinate = float(vals[2])


@section_reader('VERTICES', 4)
# ToDo: Implement Vertices Reader
def read_vertices(network: Network, block: list):
    """Reads Link vertices from block.

    Args:
      network: OOPNET network object where the coordinates shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading Vertices section')
    for vals in block:
        vals = vals['values']
        j = get_link(network, vals[0])
        v = Vertex(float(vals[1]), float(vals[2]))
        j.vertices.append(v)


@section_reader('LABELS', 4)
# ToDo: Implement Labelreader
def read_labels(network: Network, block: list):
    """

    Args:
      network: Network: 
      block: list: 

    Returns:

    """
    pass


@section_reader('BACKDROP', 4)
# ToDo: Implement Backdrop Reader
def read_backdrop(network: Network, block: list):
    """

    Args:
      network: Network: 
      block: list: 

    Returns:

    """
    pass


@section_reader('TAGS', 4)
# ToDo: Implement Tagreader
def read_tags(network: Network, block: list):
    """

    Args:
      network: Network: 
      block: list: 

    Returns:

    """
    pass
