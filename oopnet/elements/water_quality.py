from __future__ import annotations
from typing import Union, Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from oopnet.elements.network_components import Pipe


# todo: switch bulk, wall and tank to Optional[list[Pipe]]?
# todo: add attribute documentation
@dataclass
class Reaction:
    """Defines parameters related to chemical reactions occurring in the network."""
    orderbulk: Optional[float] = None
    orderwall: Optional[float] = None
    ordertank: Optional[float] = None
    globalbulk: Optional[float] = None
    globalwall: Optional[float] = None
    bulk: Union[None, Pipe, list[Pipe]] = None
    wall: Union[None, Pipe, list[Pipe]] = None
    tank: Union[None, Pipe, list[Pipe]] = None
    limitingpotential: Optional[float] = None
    roughnesscorrelation: Optional[float] = None
