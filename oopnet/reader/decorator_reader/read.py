import re
from ...elements.network import Network
from ...elements.options_and_reporting import Report, Times
from .module_reader import list_all_functions_with_decorator
from . import read_network_components, read_network_map_tags, read_options_and_reporting, \
    read_system_operation, read_water_quality
from ...utils.unit_converter.convert import convert



def filesplitter(filename):

    with open(filename, 'r') as fid:
        content = fid.readlines()
        blocks = dict()
        blockname = 'TITLE'
        blocks[blockname] = []
        for line in content:
            line = re.sub(r'\s+', ' ', line.replace('\n', '').strip())
            if line and not line.startswith(';'):
                if line.startswith('['):
                    blockname = line[1:-1]
                    blocks[blockname] = []
                else:
                    vals = dict()
                    vals['values'] = line.split(';')[0].strip().split(' ')
                    if len(line.split(';')) == 2:
                        vals['comments'] = line.split(';')[1].strip()
                    else:
                        vals['comments'] = None
                    blocks[blockname].append(vals)
    return blocks


def read(filename):
    """
    Function reads an EPAnet Input file and returns a network object

    :param filename: filename of the Epanet Input File
    :return: network object
    """

    modules = [read_network_components, read_network_map_tags, read_options_and_reporting,
               read_system_operation, read_water_quality]

    all_functions = list_all_functions_with_decorator(modules, 'section_reader')

    network = Network()

    blocks = filesplitter(filename)

    newlist = sorted(all_functions, key=lambda x: x.priority)
    for f in newlist:
        if f.sectionname in list(blocks.keys()):
            f.readerfunction(network, blocks[f.sectionname])

    # Sorting the network elements by name to guarantee same sorting everytime the read function is called
    if network.junctions:
        network.junctions.sort(key=lambda x: x.id)
    if network.reservoirs:
        network.reservoirs.sort(key=lambda x: x.id)
    if network.tanks:
        network.tanks.sort(key=lambda x: x.id)
    if network.pipes:
        network.pipes.sort(key=lambda x: x.id)
    if network.pumps:
        network.pumps.sort(key=lambda x: x.id)
    if network.valves:
        network.valves.sort(key=lambda x: x.id)

    # Generating a graph object in the network
    # Graph(network)

    # set network report if there exists no report section in the input file
    if not network.report:
        network.report = Report()

    # set network times if there exists no times section in the input file
    if not network.times:
        network.times = Times()

    # Convert network to SI units:
    convert(network)

    return network
