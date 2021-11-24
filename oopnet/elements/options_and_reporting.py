import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Union
from .network_components import Node, Pattern, Link

# todo: add default values


@dataclass
class Options:
    """
    Defines various simulation options.
    """

    units: str = 'LPS'  # = Enum('CFS', 'GPM', 'MGD', 'IMGD', 'AFD', 'LPS', 'LPM', 'MLD', 'CMH', 'CMD')
    headloss: str = 'D-W' # = Enum('H-W', 'D-W', 'C-M')
    hydraulics: Optional[List[str]] = None  # = Either(None, List('USE', Str), List('SAVE', Str))
    quality: Optional[Union[str, list]] = None  # = Any #Either(None, Enum('NONE', 'CHEMICAL', 'AGE'), List('TRACE', Instance(Node)), List('CHEMICAL', Str, Str))
    viscosity: Optional[float] = 1.0
    diffusivity: Optional[float] = 1.0
    specificgravity: Optional[float] = 1.0
    trials: Optional[int] = 200
    accuracy: Optional[float] = 0.001
    unbalanced: Union[str, List[str]] = field(default_factory=lambda: ['CONTINUE', '10']) # = Either(Enum('STOP', 'CONTINUE'), List('CONTINUE', Int))
    pattern: Optional[Union[int, Pattern]] = None
    tolerance: Optional[float] = 0.01
    map: Optional[str] = None
    demandmultiplier: Optional[float] = 1.0
    emitterexponent: Optional[float] = 0.5
    demandmodel: str = 'DDA'
    minimumpressure: Optional[float] = None
    requiredpressure: Optional[float] = None
    pressureexponent: Optional[float] = None


@dataclass
class Times:
    """Defines various time step parameters used in the simulation."""
    duration: Union[float, datetime.timedelta] = 0.0
    hydraulictimestep: Union[float, datetime.timedelta] = 1.0
    qualitytimestep: Union[float, datetime.timedelta] = 0.1
    ruletimestep: Union[float, datetime.timedelta] = 0.1
    patterntimestep: Union[float, datetime.timedelta] = 1
    patternstart: Union[float, datetime.timedelta] = 0
    reporttimestep: Union[float, datetime.timedelta] = 1
    reportstart: Union[float, datetime.timedelta] = 0
    startclocktime: datetime.timedelta = datetime.timedelta(0)
    statistic: str = 'NONE'  # = Enum('NONE', 'AVERAGED', 'MINIMUM', 'MAXIMUM', 'RANGE')


@dataclass
class Reportparameter:
    """The parameter reporting option is used to identify which quantities are reported on, how many decimal places are
    displayed, and what kind of filtering should be used to limit the output reporting."""
    elevation: Optional[Union[str, list]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    demand: Optional[Union[str, list]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    head: Optional[Union[str, list]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    pressure: Optional[Union[str, list]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    quality: Optional[Union[str, list]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    length: Optional[Union[str, list]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    diameter: Optional[Union[str, list]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    flow: Optional[Union[str, list]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    velocity: Optional[Union[str, list]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    headloss: Optional[Union[str, list]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    setting: Optional[Union[str, list]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    reaction: Optional[Union[str, list]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    ffactor: Optional[Union[str, list]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))


@dataclass
class Reportprecision:
    elevation: Optional[int] = 2
    demand: Optional[int] = 2
    head: Optional[int] = 2
    pressure: Optional[int] = 2
    quality: Optional[int] = 2
    length: Optional[int] = 2
    diameter: Optional[int] = 2
    flow: Optional[int] = 2
    velocity: Optional[int] = 2
    headloss: Optional[int] = 2
    position: Optional[int] = 2
    setting: Optional[int] = 2
    reaction: Optional[int] = 2
    ffactor: Optional[int] = 2


@dataclass
class Report:
    """Describes the contents of the output report produced from a simulation."""
    pagesize: Optional[int] = None
    file: Optional[str] = None
    status: Optional[str] = None  # = Either(None, Enum('YES', 'NO', 'FULL'))
    summary: Optional[str] = None  # = Either(None, Enum('YES', 'NO'))
    energy: Optional[str] = None  # = Either(None, Enum('YES', 'NO'))
    nodes: Optional[Union[str, Node, List[Node]]] = 'NONE'  # = Either(None, Enum('NONE', 'ALL'), Instance(Node), List(Instance(Node)))
    links: Optional[Union[str, Link, List[Link]]] = 'NONE' # = Either(None, Enum('NONE', 'ALL'), Instance(Link), List(Instance(Link)))
    parameter: Optional[str] = None  # = Either(None, Enum('YES', 'NO', 'BELOW', 'ABOVE', 'PRECISION'))
    value: Optional[float] = None  # = Either(None, Float)
