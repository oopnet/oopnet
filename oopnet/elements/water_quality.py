from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from oopnet.elements.network_components import Pipe


# todo: switch bulk, wall and tank to Optional[list[Pipe]]?
# todo: add attribute documentation
@dataclass
class Reaction:
    """Defines parameters related to chemical reactions occurring in the network."""
    orderbulk: float = 1.0
    orderwall: float = 1.0
    ordertank: float = 1.0
    globalbulk: float = 0.0
    globalwall: float = 0.0
    bulk: Optional[list[Pipe]] = None
    wall: Optional[list[Pipe]] = None
    tank: Optional[list[Pipe]] = None
    limitingpotential: Optional[float] = None
    roughnesscorrelation: Optional[float] = None
