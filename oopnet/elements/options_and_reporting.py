from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from oopnet.elements.network_components import Node, Pattern, Link

# todo: check default values
# todo: add documentation


@dataclass
class Options:
    """Defines various simulation options."""
    units: str = 'LPS'  # = 'GPM'  # = Enum('CFS', 'GPM', 'MGD', 'IMGD', 'AFD', 'LPS', 'LPM', 'MLD', 'CMH', 'CMD')
    headloss: str = 'H-W'  # str = 'H-W'  # = Enum('H-W', 'D-W', 'C-M')
    hydraulics: Optional[tuple[str, str]] = None  # = Either(None, List('USE', Str), List('SAVE', Str))
    quality: Union[str, tuple[str, str], tuple[str, str, str]] = 'NONE'  # = Any #Either(None, Enum('NONE', 'CHEMICAL', 'AGE'), List('TRACE', Instance(Node)), List('CHEMICAL', Str, Str))
    viscosity: float = 1.0
    diffusivity: float = 1.0
    specificgravity: Optional[float] = 1.0
    trials: int = 200
    accuracy: float = 0.001
    unbalanced: Union[str, tuple[str, int]] = 'STOP'  # = Either(Enum('STOP', 'CONTINUE'), List('CONTINUE', Int))
    pattern: Union[int, Pattern, None] = 1.0
    tolerance: float = 0.01
    map: Optional[str] = None
    demandmultiplier: float = 1.0
    emitterexponent: float = 0.5
    demandmodel: str = 'DDA'
    minimumpressure: float = 0.0
    requiredpressure: float = 0.1
    pressureexponent: float = 0.5


@dataclass
class Times:
    """Defines various time step parameters used in the simulation."""
    duration: datetime.timedelta = field(default=datetime.timedelta())
    hydraulictimestep: datetime.timedelta = field(default=datetime.timedelta(hours=1))
    qualitytimestep: Optional[datetime.timedelta] = None  # todo: correct qualitytimestep and ruletimestep
    # _qualitytimestep: datetime.timedelta = field(init=False, repr=False)
    ruletimestep: Optional[datetime.timedelta] = None
    patterntimestep: Optional[datetime.timedelta] = None
    patternstart: datetime.timedelta = field(default=datetime.timedelta())
    reporttimestep: datetime.timedelta = datetime.timedelta(hours=1)
    reportstart: datetime.timedelta = field(default=datetime.timedelta())
    startclocktime: datetime.timedelta = field(default=datetime.timedelta())
    statistic: str = 'NONE'  # = Enum('NONE', 'AVERAGED', 'MINIMUM', 'MAXIMUM', 'RANGE')
    
    # @property
    # def qualitytimestep(self):
    #     if not self._qualitytimestep:
    #         qts = self.qualitytimestep.total_seconds()
    #         min = np.flooar(qts / 60)
    #         h = np.floor(min / 60)
    #         s = qts - min * 60 + h * 60 ** 2
    #         return datetime.timedelta(hours=h, minutes=min, seconds=s)
    #     else:
    #         return self._qualitytimestep
    #     
    # @qualitytimestep.setter
    # def qualitstimestep(self, value):
    #     self._qualitytimestep = value
        

@dataclass
class Reportparameter:
    """The parameter reporting option is used to identify which quantities are reported on, how many decimal places are
    displayed, and what kind of filtering should be used to limit the output reporting.

    Attributes:

    """
    elevation: Union[str, tuple[str, float]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    demand: Union[str, tuple[str, float]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    head: Union[str, tuple[str, float]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    pressure: Union[str, tuple[str, float]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    quality: Union[str, tuple[str, float]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    length: Union[str, tuple[str, float]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    diameter: Union[str, tuple[str, float]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    flow: Union[str, tuple[str, float]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    velocity: Union[str, tuple[str, float]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    headloss: Union[str, tuple[str, float]] = 'YES'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    setting: Union[str, tuple[str, float]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    reaction: Union[str, tuple[str, float]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    ffactor: Union[str, tuple[str, float]] = 'NO'  # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))


@dataclass
class Reportprecision:
    """Describes the precision per report parameter."""
    elevation: int = 2
    demand: int = 2
    head: int = 2
    pressure: int = 2
    quality: int = 2
    length: int = 2
    diameter: int = 2
    flow: int = 2
    velocity: int = 2
    headloss: int = 2
    setting: int = 2
    reaction: int = 2
    ffactor: int = 2


@dataclass
class Report:
    """Describes the contents of the output report produced from a simulation."""
    pagesize: int = 0
    file: Optional[str] = None
    status: str = 'NO'  # = Either(None, Enum('YES', 'NO', 'FULL'))
    summary: str = 'YES'  # = Either(None, Enum('YES', 'NO'))
    energy: str = 'NO'  # = Either(None, Enum('YES', 'NO'))
    nodes: Union[str, Node, list[Node]] = 'ALL'  # = Either(None, Enum('NONE', 'ALL'), Instance(Node), List(Instance(Node)))
    links: Union[str, Link, list[Link]] = 'ALL'  # = Either(None, Enum('NONE', 'ALL'), Instance(Link), List(Instance(Link)))
    parameter: Union[str, tuple[str, float]] = None  # = Either(None, Enum('YES', 'NO', 'BELOW', 'ABOVE', 'PRECISION'))
    value: Optional[float] = None  # = Either(None, Float)
