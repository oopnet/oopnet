import datetime
from dataclasses import dataclass, field
from typing import List, Union, Optional

from oopnet.elements.base import NetworkComponent


# @dataclass
@dataclass(slots=True)
class Curve(NetworkComponent):
    """Defines data curves and their X,Y points."""
    xvalues: List[float] = field(default_factory=list)
    yvalues: List[float] = field(default_factory=list)


# @dataclass
@dataclass(slots=True)
class Pattern(NetworkComponent):
    """Defines time patterns."""
    multipliers: List = field(default_factory=list)


# @dataclass
@dataclass(slots=True)
class Energy:
    """Defines parameters used to compute pumping energy and cost."""

    keyword: str = None  # = Enum('GLOBAL', 'PUMP', 'DEMAND CHARGE')
    pumpid: NetworkComponent = None  # = Instance(NetworkComponent)  # ToDo: pipeid self referencing on pump class instead of NetworkComponent
    parameter: str = None  # = Either(None, Enum('PRICE', 'EFFIC', 'PATTERN', 'EFFICIENCY'))
    value: Union[float, Pattern, Curve] = None  # = Either(Float, Instance(Pattern), Instance(Curve))


# @dataclass
@dataclass(slots=True)
class Condition:
    """A condition clause in a rule-based control"""
    # ToDo: object attribute should be either instance of Node or Link instead of Network Component
    object: NetworkComponent
    # __object = Either(Instance(Node), Instance(Link))
    logical: str  # = Either('IF', 'AND', 'OR', 'THEN', 'ELSE')
    attribute: str # = Enum('DEMAND', 'HEAD', 'PRESSURE', 'LEVEL', 'FILLTIME', 'DRAINTIME', 'FLOW', 'STATUS', 'SETTING',
                   #    'TIME', 'CLOCKTIME')
    relation: str  #  = Enum('=', '<>', '<', '>', '<=', '>=', 'IS', 'NOT', 'BELOW', 'ABOVE')
    value: Union[float, str, datetime.datetime, datetime.timedelta]  # = Either(Float, Enum('OPEN', 'CLOSED'), Instance(datetime.datetime), Instance(datetime.timedelta))


# @dataclass
@dataclass(slots=True)
class Action:
    """An action clause in a rule-based control"""
    # ToDo: object attribute should be either instance of Node or Link instead of Network Component
    object: Union[NetworkComponent, str]  # = Either(NetworkComponent, 'SYSTEM')
    # __object = Either(Instance(Node), Instance(Link), 'SYSTEM')
    value: Union[float, str]  # = Either(Float, Enum('OPEN', 'CLOSED'))


# @dataclass
@dataclass(slots=True)
class Rule:
    """Defines rule-based controls that modify links based on a combination of conditions."""
    id: str
    condition: Union[Condition, List[Condition]]  # = Either(Instance(Condition), List(Instance(Condition)))
    priority: float


# @dataclass
@dataclass(slots=True)
class Controlcondition:
    """ """

    # ToDo: object attribute should be either instance of Node instead of Network Component
    object: Optional[NetworkComponent] = None
    # __object = Instance(Node)
    relation: Optional[str] = None  #  = Enum('ABOVE', 'BELOW')
    value: Optional[float] = None
    time: Union[None, float, datetime.timedelta] = None
    clocktime: Optional[datetime.datetime] = None


# @dataclass
@dataclass(slots=True)
class Control:

    """Defines simple controls that modifiy links based on a single condition."""
    action: Action
    condition: Controlcondition
