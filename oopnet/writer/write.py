from oopnet.elements.network import Network

from oopnet.writer.module_reader import list_all_functions_with_decorator
from oopnet.writer import write_network_map_tags, write_options_and_reporting, write_network_components, \
    write_water_quality, write_system_operation


def write(network: Network, filename: str) -> int:
    """Converts an OOPNET network function to an EPANET input file and saves it with a desired filename.

    Args:
      network: OOPNET network object which one wants to be written to a file
      filename: desired filename/path were the user wants to store the file

    Returns:
      0

    """

    modules = [write_network_components, write_network_map_tags, write_options_and_reporting,
               write_system_operation, write_water_quality]

    all_functions = list_all_functions_with_decorator(modules, 'section_writer')

    newlist = sorted(all_functions, key=lambda x: x.priority)

    with open(filename, 'w') as fid:
        for f in newlist:
            f.writerfunction(network, fid)

    return 0
