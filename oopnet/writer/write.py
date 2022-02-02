from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from oopnet.writer.module_reader import list_section_writer_callables
from oopnet.writer.writing_modules import write_system_operation, write_network_map_tags, write_water_quality, \
    write_options_and_reporting, write_network_components
from oopnet.utils.oopnet_logging import logging_decorator
if TYPE_CHECKING:
    from oopnet.elements.network import Network

logger = logging.getLogger(__name__)


@logging_decorator(logger)
def write(network: Network, filename: str) -> int:
    """Converts an OOPNET network to an EPANET input file and saves it with a desired filename.

    Args:
      network: OOPNET network object which one wants to be written to a file
      filename: desired filename/path were the user wants to store the file

    Returns:
      0 if successful

    """
    logger.info(f'Writing network to {filename!r}')

    modules = [write_network_components, write_network_map_tags, write_options_and_reporting,
               write_system_operation, write_water_quality]

    all_functions = list_section_writer_callables(modules)

    newlist = sorted(all_functions, key=lambda x: x.priority)
    with open(filename, 'w') as fid:
        for f in newlist:
            f.writerfunction(network, fid)

    return 0
