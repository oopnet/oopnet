from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from oopnet.elements.network_components import Junction, Tank, Reservoir, Pipe, Pump, Valve
from oopnet.utils.getters import get_node, get_link
from oopnet.utils.oopnet_logging import logging_decorator
if TYPE_CHECKING:
    from oopnet.elements.network import Network

logger = logging.getLogger(__name__)


@logging_decorator(logger)
def _remove_object(hash_dict: dict, id: str):
    if id not in hash_dict:
        raise ValueError(f'No object with ID {id} found.')
    logger.debug(f'Removing object with ID {id}')
    hash_dict.pop(id)


def remove_link(network: Network, id: str):
    """This function removes a specific Link from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Link ID

    """
    l = get_link(network, id)
    if isinstance(l, Pipe):
        remove_pipe(network, id)
    elif isinstance(l, Pump):
        remove_pump(network, id)
    elif isinstance(l, Valve):
        remove_valve(network, id)


# todo: remove Links connected to Node?
def remove_node(network: Network, id: str):
    """This function removes a specific Node from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Node ID

    """
    n = get_node(network, id)
    if isinstance(n, Junction):
        remove_junction(network, id)
    elif isinstance(n, Tank):
        remove_tank(network, id)
    elif isinstance(n, Reservoir):
        remove_reservoir(network, id)


def remove_junction(network: Network, id: str):
    """This function removes a specific Junction from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Junction ID

    """
    _remove_object(network._nodes['junctions'], id)


def remove_reservoir(network: Network, id: str):
    """This function removes a specific Reservoir from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Reservoir ID

    """
    _remove_object(network._nodes['reservoirs'], id)


def remove_tank(network: Network, id: str):
    """This function removes a specific Tank from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Tank ID

    """
    _remove_object(network._nodes['tanks'], id)


def remove_pipe(network: Network, id: str):
    """This function removes a specific Pipe from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Pipe ID

    """
    _remove_object(network._links['pipes'], id)


def remove_pump(network: Network, id: str):
    """This function removes a specific Pump from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Pump ID

    """
    _remove_object(network._links['pumps'], id)


def remove_valve(network: Network, id: str):
    """This function removes a specific Valve from an OOPNET network.

    Args:
      network: OOPNET network object
      id: Valve ID

    """
    _remove_object(network._links['valves'], id)
