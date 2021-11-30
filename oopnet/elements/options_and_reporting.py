import datetime
from dataclasses import dataclass
from typing import List, Optional, Union

from oopnet.elements.network_components import Node, Pattern, Link

# todo: check default values


@dataclass
class Options:
    """Defines various simulation options."""
    units: str = 'GPM'  # = Enum('CFS', 'GPM', 'MGD', 'IMGD', 'AFD', 'LPS', 'LPM', 'MLD', 'CMH', 'CMD')
    headloss: str = 'H-W'  # = Enum('H-W', 'D-W', 'C-M')
    hydraulics: Optional[List[str]] = None  # = Either(None, List('USE', Str), List('SAVE', Str))
    quality: Union[str, list, None] = None  # = Any #Either(None, Enum('NONE', 'CHEMICAL', 'AGE'), List('TRACE', Instance(Node)), List('CHEMICAL', Str, Str))
    viscosity: Optional[float] = None
    diffusivity: Optional[float] = None
    specificgravity: Optional[float] = None
    trials: Optional[int] = None
    accuracy: Optional[float] = None
    unbalanced: Union[str, List[str]] = None  # = Either(Enum('STOP', 'CONTINUE'), List('CONTINUE', Int))
    pattern: Union[int, Pattern, None] = None
    tolerance: Optional[float] = None
    map: Optional[str] = None
    demandmultiplier: Optional[float] = None
    emitterexponent: Optional[float] = None
    demandmodel: str = 'DDA'
    minimumpressure: Optional[float] = None
    requiredpressure: Optional[float] = None
    pressureexponent: Optional[float] = None


@dataclass
class Times:
    """Defines various time step parameters used in the simulation."""
    duration: datetime.timedelta = None
    hydraulictimestep: datetime.timedelta = None
    qualitytimestep: datetime.timedelta = None
    ruletimestep: datetime.timedelta = None
    patterntimestep: datetime.timedelta = None
    patternstart: datetime.timedelta = None
    reporttimestep: datetime.timedelta = None
    reportstart: datetime.timedelta = None
    startclocktime: datetime.timedelta = None
    statistic: str = 'NONE'  # = Enum('NONE', 'AVERAGED', 'MINIMUM', 'MAXIMUM', 'RANGE')


@dataclass
class Reportparameter:
    """The parameter reporting option is used to identify which quantities are reported on, how many decimal places are
    displayed, and what kind of filtering should be used to limit the output reporting.

    Attributes:

    """
    elevation: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    demand: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    head: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    pressure: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    quality: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    length: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    diameter: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    flow: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    velocity: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    headloss: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    setting: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    reaction: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    ffactor: Union[str, list, None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))


@dataclass
class Reportprecision:
    """Describes the precision per report parameter."""
    elevation: Optional[int] = None
    demand: Optional[int] = None
    head: Optional[int] = None
    pressure: Optional[int] = None
    quality: Optional[int] = None
    length: Optional[int] = None
    diameter: Optional[int] = None
    flow: Optional[int] = None
    velocity: Optional[int] = None
    headloss: Optional[int] = None
    position: Optional[int] = None
    setting: Optional[int] = None
    reaction: Optional[int] = None
    ffactor: Optional[int] = None


@dataclass
class Report:
    """Describes the contents of the output report produced from a simulation."""
    pagesize: Optional[int] = None
    file: Optional[str] = None
    status: Optional[str] = None  # = Either(None, Enum('YES', 'NO', 'FULL'))
    summary: Optional[str] = None  # = Either(None, Enum('YES', 'NO'))
    energy: Optional[str] = None  # = Either(None, Enum('YES', 'NO'))
    nodes: Union[str, Node, List[Node], None] = None  # = Either(None, Enum('NONE', 'ALL'), Instance(Node), List(Instance(Node)))
    links: Union[str, Link, List[Link], None] = None # = Either(None, Enum('NONE', 'ALL'), Instance(Link), List(Instance(Link)))
    parameter: Optional[str] = None  # = Either(None, Enum('YES', 'NO', 'BELOW', 'ABOVE', 'PRECISION'))
    value: Optional[float] = None  # = Either(None, Float)
