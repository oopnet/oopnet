"""
This module contains all the base classes of OOPNET
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

from oopnet.exceptions import ComponentExistsError


@dataclass
class NetworkComponent:
    """This is OOPNET's base class for all objects having a name (id) in EPANET Input files

    Attributes:
      id: A unique label used to identify the Network Component. It can consist of a combination of up to 15 numerals or characters. It cannot be the same as the ID for any other node if it is a node, the same counts for links.
      comment: Property containing a comment on the attribute if it is necessary. The comment is automatically read in from EPANET input files by parsing everything behind a semicolon (;), if a semicolon is not the first character in a line
      tag: Associates category labels (tags) with specific nodes and links. An optional text string (with no spaces) used to assign e.g. the node to a category, such as a pressure zone.

    """
    id: str
    _id: str = field(init=False, repr=False)
    comment: Optional[str] = None
    tag: Optional[str] = None
    _component_hash: dict = None

    def __str__(self):
        return self.id

    def __hash__(self):
        return hash(self.id) + hash(type(self))

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets ID of NetworkComponent and replaces key in network hash"""
        if self._component_hash:
            if id in self._component_hash:
                raise ComponentExistsError(id)
            self._component_hash[id] = self
            del self._component_hash[self._id]
        self._id = id


# todo: seperate file
class BoolSetting(str, Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'


class PipeStatus(str, Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    CV = 'CV'


class ValveStatus(str, Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    ACTIVE = 'ACTIVE'


class PumpStatus(str, Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'


class MixingModel(str, Enum):
    MIXED = 'MIXED'
    TWOCOMP = '2COMP'
    FIFO = 'FIFO'
    LIFO = 'LIFO'


class Unit(str, Enum):
    CFS = 'CFS'
    GPM = 'GPM'
    MGD = 'MGD'
    IMGD = 'IMGD'
    AFD = 'AFD'
    LPS = 'LPS'
    LPM = 'LPM'
    MLD = 'MLD'
    CMH = 'CMH'
    CMD = 'CMD'


# todo: rename?
class HeadlossFormula(str, Enum):
    HW = 'H-W'
    DW = 'D-W'
    CM = 'C-M'

    @classmethod
    def parse(cls, string: str):
        return cls[string.replace('-', '')]


# todo: rethink name
class PumpKeyword(str, Enum):
    POWER = 'POWER'
    HEAD = 'HEAD'
    SPEED = 'SPEED'
    PATTERN = 'PATTERN'


class ValveType(str, Enum):
    PRV = 'PRV'
    PSV = 'PSV'
    PBV = 'PBV'
    FCV = 'FCV'
    TCV = 'TCV'
    GPV = 'GPV'


class TagObject(str, Enum):
    NODE = 'NODE'
    LINK = 'LINK'


class HydraulicOption(str, Enum):
    USE = 'USE'
    SAVE = 'SAVE'


class QualityOption(str, Enum):
    NONE = 'NONE'
    CHEMICAL = 'CHEMICAL'
    AGE = 'AGE'
    TRACE = 'TRACE'


class BalancingOption(str, Enum):
    STOP = 'STOP'
    CONTINUE = 'CONTINUE'


class DemandModel(str, Enum):
    DDA = 'DDA'
    PDA = 'PDA'


class StatisticSetting(str, Enum):
    NONE = 'NONE'
    AVERAGED = 'AVERAGED'
    MINIMUM = 'MINIMUM'
    MAXIMUM = 'MAXIMUM'
    RANGE = 'RANGE'


class LimitSetting(str, Enum):
    BELOW = 'BELOW'
    ABOVE = 'ABOVE'


class ReportStatusSetting(str, Enum):
    YES = 'YES'
    NO = 'NO'
    FULL = 'FULL'


class ReportBoolSetting(str, Enum):
    YES = 'YES'
    NO = 'NO'


class ReportElementSetting(str, Enum):
    NONE = 'NONE'
    ALL = 'ALL'


class ReportParameterSetting(str, Enum):
    YES = 'YES'
    NO = 'NO'
    BELOW = 'BELOW'
    ABOVE = 'ABOVE'
    PRECISION = 'PRECISION'


class EnergyKeyword(str, Enum):
    GLOBAL = 'GLOBAL'
    PUMP = 'PUMP'


class EnergyParameter(str, Enum):
    PRICE = 'PRICE'
    EFFICIENCY = 'EFFICIENCY'
    PATTERN = 'PATTERN'
    DEMAND_CHARGE = 'DEMAND CHARGE'


class Logic(str, Enum):
    IF = 'IF'
    AND = 'AND'
    OR = 'OR'
    THEN = 'THEN'
    ELSE = 'ELSE'


class Relation(str, Enum):
    GREATER = '>'
    GREATER_EQUAL = '>='
    LOWER = '<'
    LOWER_EQUAL = '<='
    EQUAL = '='
    NOT_EQUAL = '<>'

    @classmethod
    def parse(cls, string: str):
        if string in {'IS', '='}:
            return cls.EQUAL
        elif string in {'BELOW', '<'}:
            return cls.LOWER
        elif string in {'ABOVE', '>'}:
            return cls.GREATER
        elif string in {'NOT', '<>'}:
            return cls.NOT_EQUAL
        elif string == '>=':
            return cls.GREATER_EQUAL
        elif string == '<=':
            return cls.LOWER_EQUAL
        else:
            return cls[string]


class ConditionAttribute(str, Enum):
    DEMAND = 'DEMAND'
    HEAD = 'HEAD'
    PRESSURE = 'PRESSURE'
    LEVEL = 'LEVEL'
    FILLTIME = 'FILLTIME'
    DRAINTIME = 'DRAINTIME'
    FLOW = 'FLOW'
    STATUS = 'STATUS'
    SETTING = 'SETTING'
    TIME = 'TIME'
    CLOCKTIME = 'CLOCKTIME'
