from __future__ import annotations
import re
import logging
from typing import Optional, TYPE_CHECKING

from oopnet.reader.unit_converter.convert import convert
from oopnet.reader.module_reader import list_section_reader_callables
from oopnet.reader.reading_modules import read_system_operation, read_options_and_reporting, read_network_components, \
    read_network_map_tags, read_water_quality
from oopnet.utils.oopnet_logging import logging_decorator
if TYPE_CHECKING:
    from oopnet.elements.network import Network

logger = logging.getLogger(__name__)


def filesplitter(content: list[str]) -> dict[str, list]:
    """Reads an EPANET input file and splits the content into blocks.

    Args:
      content: EPANET input file content as str

    Returns:
        blocks

    """

    blocks = {}
    blockname = 'TITLE'
    blocks[blockname] = []
    for line in content:
        line = re.sub(r'\s+', ' ', line.replace('\n', '').strip())
        if line and not line.startswith(';'):
            if line.startswith('['):
                blockname = line[1:-1]
                blocks[blockname] = []
            else:
                vals = {'values': line.split(';')[0].strip().split(' ')}
                if len(line.split(';')) == 2:
                    vals['comments'] = line.split(';')[1].strip()
                else:
                    vals['comments'] = None
                blocks[blockname].append(vals)
    return blocks


@logging_decorator(logger)
def read(network: Network, filename: Optional[str] = None, content: Optional[str] = None) -> Network:
    """Function reads an EPANET input file and returns a network object.

    Args:
      filename: filename of the EPANET input file

    Returns:
      network object

    """
    modules = [read_network_components, read_network_map_tags, read_options_and_reporting,
               read_system_operation, read_water_quality]

    all_functions = list_section_reader_callables(modules)

    if filename:
        logger.info(f'Reading model from {filename!r}')
        with open(filename, 'r') as fid:
            content = fid.readlines()
    elif content:
        logger.info('Reading model from passed string')
        content = content.splitlines()
    else:
        raise ValueError('Either one of the arguments "filename" or "content" have to be provided.')

    blocks = filesplitter(content)
    newlist = sorted(all_functions, key=lambda x: x.priority)
    for f in newlist:
        if f.sectionname in list(blocks.keys()):
            f.readerfunction(network, blocks[f.sectionname])

    # Convert network to SI units
    convert(network)

    return network
