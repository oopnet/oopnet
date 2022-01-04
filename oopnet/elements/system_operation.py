import datetime
from dataclasses import dataclass, field
from typing import List, Union, Optional

from oopnet.elements.base import NetworkComponent, LimitSetting, EnergyParameter, EnergyKeyword, Logic, \
    ConditionAttribute, BoolSetting, Relation
# from oopnet.elements.network_components import Node, Link

# todo: refactor reader to allow for mandatory attributes
@dataclass
class Curve(NetworkComponent):
    """Defines data curves and their X,Y points."""
    xvalues: List[float] = field(default_factory=list)
    yvalues: List[float] = field(default_factory=list)


@dataclass
class Pattern(NetworkComponent):
    """Defines time patterns."""
    multipliers: List = field(default_factory=list)


# todo: rethink implementation -> move pump specific settings to Pump class and global settings to Network?
@dataclass
class Energy:
    """Defines parameters used to compute pumping energy and cost."""

    keyword: Optional[EnergyKeyword] = None  # = Enum('GLOBAL', 'PUMP', 'DEMAND CHARGE')
    pumpid: Optional[NetworkComponent] = None  # = Instance(NetworkComponent)  # ToDo: pipeid self referencing on pump class instead of NetworkComponent
    parameter: Optional[EnergyParameter] = None  # = Either(None, Enum('PRICE', 'EFFIC', 'PATTERN', 'EFFICIENCY'))
    value: Union[float, Pattern, Curve] = None  # = Either(Float, Instance(Pattern), Instance(Curve))


@dataclass
class Condition:
    """A condition clause in a rule-based control"""
    object: Union['Link', 'Node'] = None
    logical: Optional[Logic] = None # = Either('IF', 'AND', 'OR', 'THEN', 'ELSE')
    attribute: ConditionAttribute = None # = Enum('DEMAND', 'HEAD', 'PRESSURE', 'LEVEL', 'FILLTIME', 'DRAINTIME', 'FLOW', 'STATUS', 'SETTING',
                   #    'TIME', 'CLOCKTIME')
    relation: Relation = None  #  = Enum('=', '<>', '<', '>', '<=', '>=', 'IS', 'NOT', 'BELOW', 'ABOVE')
    value: Union[float, BoolSetting, datetime.datetime, datetime.timedelta] = None  # = Either(Float, Enum('OPEN', 'CLOSED'), Instance(datetime.datetime), Instance(datetime.timedelta))


@dataclass
class Action:
    """An action clause in a rule-based control"""
    # ToDo: object attribute should be either instance of Node or Link -> circular import
    object: Union['Node', 'Link', str] = None  # = Either(NetworkComponent, 'SYSTEM')
    value: Union[float, BoolSetting] = None  # = Either(Float, Enum('OPEN', 'CLOSED'))


@dataclass
class Rule:
    """Defines rule-based controls that modify links based on a combination of conditions."""
    id: str
    condition: Union[Condition, List[Condition]] = None  # = Either(Instance(Condition), List(Instance(Condition)))
    priority: float = None


@dataclass
class Controlcondition:
    """ """
    # ToDo: object attribute should be either instance of Node instead of Network Component
    object: Optional[NetworkComponent] = None
    # __object = Instance(Node)
    relation: Optional[LimitSetting] = None  #  = Enum('ABOVE', 'BELOW')
    value: Optional[float] = None
    time: Union[None, float, datetime.timedelta] = None
    clocktime: Optional[datetime.datetime] = None


@dataclass
class Control:
    """Defines simple controls that modifiy links based on a single condition."""
    action: Action = None
    condition: Controlcondition = None
