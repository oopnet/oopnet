from __future__ import annotations
import datetime
from dataclasses import dataclass, field
from typing import Union, Optional, TYPE_CHECKING

from oopnet.elements.base import NetworkComponent


if TYPE_CHECKING:
    from oopnet.elements.network_components import Node, Link


# todo: refactor reader to allow for mandatory attributes
# todo: add attribute documentation
@dataclass
class Curve(NetworkComponent):
    """Defines data curves and their X,Y points."""
    xvalues: list[float] = field(default_factory=list)
    yvalues: list[float] = field(default_factory=list)

    @NetworkComponent.id.setter
    def id(self, id: str):
        """Sets ID of NetworkComponent and replaces key in network hash"""
        if self._network:
            self._rename(id=id, hashtable=self._network._curves)
        self._id = id

@dataclass
class Pattern(NetworkComponent):
    """Defines time patterns."""
    multipliers: list[float] = field(default_factory=list)

    @NetworkComponent.id.setter
    def id(self, id: str):
        """Sets ID of NetworkComponent and replaces key in network hash"""
        if self._network:
            self._rename(id=id, hashtable=self._network._patterns)
        self._id = id


# todo: rethink implementation -> move pump specific settings to Pump class and global settings to Network?
@dataclass
class Energy:
    """Defines parameters used to compute pumping energy and cost."""

    keyword: Optional[str] = None  # = Enum('GLOBAL', 'PUMP', 'DEMAND CHARGE')
    pumpid: Optional[str] = None  # = Instance(NetworkComponent)  # ToDo: pipeid self referencing on pump class instead of NetworkComponent
    parameter: Optional[str] = None  # = Either(None, Enum('PRICE', 'EFFIC', 'PATTERN', 'EFFICIENCY'))
    value: Union[float, Pattern, Curve] = None  # = Either(Float, Instance(Pattern), Instance(Curve))


@dataclass
class Condition:
    """A condition clause in a rule-based control"""
    object: Union[Link, Node] = None
    logical: Optional[str] = None # = Either('IF', 'AND', 'OR', 'THEN', 'ELSE')
    attribute: str = None # = Enum('DEMAND', 'HEAD', 'PRESSURE', 'LEVEL', 'FILLTIME', 'DRAINTIME', 'FLOW', 'STATUS', 'SETTING',
                   #    'TIME', 'CLOCKTIME')
    relation: str = None  #  = Enum('=', '<>', '<', '>', '<=', '>=', 'IS', 'NOT', 'BELOW', 'ABOVE')
    value: Union[float, str, datetime.datetime, datetime.timedelta] = None  # = Either(Float, Enum('OPEN', 'CLOSED'), Instance(datetime.datetime), Instance(datetime.timedelta))


@dataclass
class Action:
    """An action clause in a rule-based control"""
    object: Union[Node, Link, str] = None  # = Either(NetworkComponent, 'SYSTEM')
    value: Union[float, str] = None  # = Either(Float, Enum('OPEN', 'CLOSED'))


@dataclass
class Rule:
    """Defines rule-based controls that modify links based on a combination of conditions."""
    id: str
    condition: Union[Condition, list[Condition]] = None  # = Either(Instance(Condition), List(Instance(Condition)))
    priority: float = None


@dataclass
class Controlcondition:
    """ """
    # ToDo: object attribute should be either instance of Node instead of Network Component
    object: Optional[NetworkComponent] = None
    # __object = Instance(Node)
    relation: Optional[str] = None  #  = Enum('ABOVE', 'BELOW')
    value: Optional[float] = None
    time: Union[None, float, datetime.timedelta] = None
    clocktime: Optional[datetime.datetime] = None


@dataclass
class Control:
    """Defines simple controls that modifiy links based on a single condition."""
    action: Action = None
    condition: Controlcondition = None
