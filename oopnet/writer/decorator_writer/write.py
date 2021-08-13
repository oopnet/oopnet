from .module_reader import list_all_functions_with_decorator
from . import write_network_components, write_network_map_tags, write_options_and_reporting, \
    write_system_operation, write_water_quality


def write(network, filename):
    """
    This function converts an OOPNET network function to an EPANET input file and saves it with a desired filename

    :param network: OOPNET network object which one wants to be written to a file
    :param filename: desired filename/path were the user wants to store the file
    :return: 0
    """

    modules = [write_network_components, write_network_map_tags, write_options_and_reporting,
               write_system_operation, write_water_quality]

    all_functions = list_all_functions_with_decorator(modules, 'section_writer')

    newlist = sorted(all_functions, key=lambda x: x.priority)

    with open(filename, 'w') as fid:
        for f in newlist:
            f.writerfunction(network, fid)

    return 0
