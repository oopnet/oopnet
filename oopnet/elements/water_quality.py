from typing import Union, List
from dataclasses import dataclass
from ..elements.network_components import Pipe


@dataclass
class Reaction:
    """Defines parameters related to chemical reactions occuring in the network."""
    orderbulk: float
    orderwall: float
    ordertank: float
    globalbulk: float
    globalwall: float
    bulk: Union[Pipe, List[Pipe]]
    wall: Union[Pipe, List[Pipe]]
    tank: Union[Pipe, List[Pipe]]
    limitingpotential: float
    roughnesscorrelation: float
