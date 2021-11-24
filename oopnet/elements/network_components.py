from .base import NetworkComponent
from .system_operation import Pattern, Curve
from typing import List, Union, Optional
from dataclasses import dataclass


@dataclass
class Node(NetworkComponent):
    """
    Defines base class for all Node like objects in OOPNET (Junction, Reservoir, Tank)
    """
    xcoordinate: float = 0.0
    ycoordinate: float = 0.0
    initialquality: float = 0.0
    sourcequality: float = 0.0
    # todo: rethink enum type hinting for sourcetype
    sourcetype: Optional[str] = None
    strength: float = 0.0
    # todo: source pattern as general Node attribute?
    sourcepattern: Optional[List[Pattern]] = None

    @property
    def coordinates(self):
        return self.xcoordinate, self.ycoordinate, self.elevation


@dataclass
class Link(NetworkComponent):
    """
    Defines base class for all Link like objects in OOPNET (Pipe, Pump, Valve)
    """
    startnode: Optional[Node] = None
    endnode: Optional[Node] = None
    # todo: rethink enum type hinting for initialstatus and status
    initialstatus: str = 'OPEN'
    status: str = 'OPEN'
    # initialstatus = Either(None, Enum('OPEN', 'CLOSED', 'ACTIVE', 'CV'), Float)
    # status = Enum('OPEN', 'CLOSED', 'ACTIVE', 'CV')


@dataclass
class Junction(Node):
    """
    Defines Junction nodes contained in the network.
    """

    elevation: float = 0.0
    emittercoefficient: float = 0.0
    # todo: can junctions have several patterns?
    demandpattern: Optional[Pattern] = None  # = Either(Instance(Pattern), List(Instance(Pattern)))
    demand: float = 0.0
    # todo: can a junction have several floats as demand?
    # demand = Either(Float, ListFloat)


@dataclass
class Reservoir(Node):
    """
    Defines all reservoir nodes contained in the network.
    """
    head: float = None  # = Either(None, Float, ListFloat)
    headpattern: Optional[Pattern] = None  # = Either(None, Instance(Pattern), List(Instance(Pattern)))
    # todo: double check if mixing model is reservoir attribute
    mixingmodel: str = 'MIXED' # = Enum('MIXED', '2COMP', 'FIFO', 'LIFO')


@dataclass
class Tank(Node):
    """
    Defines all tank nodes contained in the network.
    """
    elevation: float = 0
    initlevel: float = 0.0
    minlevel: float = 10
    maxlevel: float = 20
    diam: float = 50
    minvolume: Optional[float] = None
    volumecurve: Optional[Curve] = None
    compartmentvolume: Optional[float] = None
    reactiontank: Optional[float] = None
    mixingmodel: str = 'MIXED'  # = Enum('MIXED', '2COMP', 'FIFO', 'LIFO')


@dataclass
class Pipe(Link):
    """
    Defines all pipe links contained in the network.
    """
    length: float = 1000
    diameter: float = 12
    roughness: float = 0.1
    minorloss: float = 0
    reactionbulk: Optional[float] = None
    reactionwall: Optional[float] = None


@dataclass
class Pump(Link):
    """
    Defines all pump links contained in the network.
    """

    keyword: Optional[str] = None  # = Enum('POWER', 'HEAD', 'SPEED', 'PATTERN')
    value: Optional[Union[str, float]] = None
    status: Optional[Union[str, float]] = None  # = Either(None, Enum('OPEN', 'CLOSED', 'ACTIVE'), Float)


@dataclass
class Valve(Link):
    """
    Defines all control valve links contained in the network
    """
    valvetype: str = 'PRV'
    diameter: float = 12
    minorloss: float = 0
    # todo: double check possible setting datatypes
    setting: Union[float, str] = 0
    # setting = Any  # ToDo: Rethink if any is correct for setting attribute


@dataclass
class PRV(Valve):
    # ToDo: Implement PRV (Pressure Reducing Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


@dataclass
class TCV(Valve):
    # ToDo: Implement TCV (Throttle Control Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


@dataclass
class PSV(Valve):
    # ToDo: Implement PSV (Pressure Sustaining Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


@dataclass
class GPV(Valve):
    # ToDo: Implement GPV (General Purpose Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


@dataclass
class PBV(Valve):
    # ToDo: Implement PBV (Pressure Breaker Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


@dataclass
class FCV(Valve):
    # ToDo: Implement FCV (Flow Control Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass
