from io import TextIOWrapper

from oopnet.utils.getters import get_nodes
from oopnet.writer.decorator_writer.decorators import section_writer
from oopnet.elements.network import Network


# todo: section doesn't have to be present for simulating with EPANET via CLI - could be omitted when creating an input file for simulations
@section_writer('COORDINATES', 4)
def write_coordinates(network: Network, fid: TextIOWrapper):
    """Writes coordinates to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[COORDINATES]', file=fid)
    print(';nodeid xcoordinate ycoordinate', file=fid)
    for n in get_nodes(network):
        print(n.id, n.xcoordinate, n.ycoordinate, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('VERTICES', 4)
def write_vertices(network: Network, fid: TextIOWrapper):
    """Writes vertices to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    # ToDo: Implement Printer for Vertices
    print('[VERTICES]', file=fid)
    print(';linkkid xcoordinate ycoordinate', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('LABELS', 4)
def write_labels(network: Network, fid: TextIOWrapper):
    """Writes labels to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    # ToDo: Implement Printer for Labels
    print('[LABELS]', file=fid)
    print(';xcoordinate ycoordinate label anchornode', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('BACKDROP', 4)
def write_backdrop(network: Network, fid: TextIOWrapper):
    """Writes backdrop data to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    # ToDo: Implement Printer for Backdrop
    print('[BACKDROP]', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('TAGS', 4)
def write_tags(network: Network, fid: TextIOWrapper):
    """Writes tags to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    # ToDo: Implement Printer for Tags
    print('[TAGS]', file=fid)
    print('\n', end=' ', file=fid)
