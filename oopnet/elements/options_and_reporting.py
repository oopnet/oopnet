from __future__ import annotations
import datetime
from dataclasses import dataclass
from typing import List, Optional, Union, Literal, Tuple

from oopnet.elements.enums import BoolSetting, Unit, HeadlossFormula, HydraulicOption, QualityOption, BalancingOption, \
    DemandModel, StatisticSetting, LimitSetting, ReportStatusSetting, ReportBoolSetting, ReportElementSetting, \
    ReportParameterSetting

from oopnet.elements.network_components import Node, Pattern, Link

# todo: check default values


@dataclass
class Options:
    """Defines various simulation options."""
    units: Unit = Unit.GPM  # = 'GPM'  # = Enum('CFS', 'GPM', 'MGD', 'IMGD', 'AFD', 'LPS', 'LPM', 'MLD', 'CMH', 'CMD')
    headloss: HeadlossFormula = HeadlossFormula.HW  # str = 'H-W'  # = Enum('H-W', 'D-W', 'C-M')
    hydraulics: Optional[Tuple[HydraulicOption, str]] = None  # = Either(None, List('USE', Str), List('SAVE', Str))
    quality: Union[QualityOption, Tuple[Literal[QualityOption.TRACE], str], Tuple[Literal[QualityOption.CHEMICAL], str, str], None] = None  # = Any #Either(None, Enum('NONE', 'CHEMICAL', 'AGE'), List('TRACE', Instance(Node)), List('CHEMICAL', Str, Str))
    viscosity: Optional[float] = None
    diffusivity: Optional[float] = None
    specificgravity: Optional[float] = None
    trials: Optional[int] = None
    accuracy: Optional[float] = None
    unbalanced: Union[BalancingOption, Tuple[Literal[BalancingOption.CONTINUE], int], None] = None  # = Either(Enum('STOP', 'CONTINUE'), List('CONTINUE', Int))
    pattern: Union[int, Pattern, None] = None
    tolerance: Optional[float] = None
    map: Optional[str] = None
    demandmultiplier: Optional[float] = None
    emitterexponent: Optional[float] = None
    demandmodel: DemandModel = DemandModel.DDA
    minimumpressure: Optional[float] = None
    requiredpressure: Optional[float] = None
    pressureexponent: Optional[float] = None


@dataclass
class Times:
    """Defines various time step parameters used in the simulation."""
    duration: Optional[datetime.timedelta] = None
    hydraulictimestep: Optional[datetime.timedelta] = None
    qualitytimestep: Optional[datetime.timedelta] = None
    ruletimestep: Optional[datetime.timedelta] = None
    patterntimestep: Optional[datetime.timedelta] = None
    patternstart: Optional[datetime.timedelta] = None
    reporttimestep: Optional[datetime.timedelta] = None
    reportstart: Optional[datetime.timedelta] = None
    startclocktime: Optional[datetime.timedelta] = None
    statistic: Optional[StatisticSetting] = StatisticSetting.NONE  # = Enum('NONE', 'AVERAGED', 'MINIMUM', 'MAXIMUM', 'RANGE')


@dataclass
class Reportparameter:
    """The parameter reporting option is used to identify which quantities are reported on, how many decimal places are
    displayed, and what kind of filtering should be used to limit the output reporting.

    Attributes:

    """
    elevation: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    demand: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    head: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    pressure: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    quality: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    length: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    diameter: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    flow: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    velocity: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    headloss: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    setting: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    reaction: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    ffactor: Union[BoolSetting, Tuple[LimitSetting, float], None] = None # = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))


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
    status: Optional[ReportStatusSetting] = None  # = Either(None, Enum('YES', 'NO', 'FULL'))
    summary: Optional[ReportBoolSetting] = None  # = Either(None, Enum('YES', 'NO'))
    energy: Optional[ReportBoolSetting] = None  # = Either(None, Enum('YES', 'NO'))
    nodes: Union[ReportElementSetting, Node, List[Node], None] = None  # = Either(None, Enum('NONE', 'ALL'), Instance(Node), List(Instance(Node)))
    links: Union[ReportElementSetting, Link, List[Link], None] = None # = Either(None, Enum('NONE', 'ALL'), Instance(Link), List(Instance(Link)))
    parameter: Union[ReportParameterSetting, Tuple[ReportParameterSetting, float], None] = None  # = Either(None, Enum('YES', 'NO', 'BELOW', 'ABOVE', 'PRECISION'))
    value: Optional[float] = None  # = Either(None, Float)
