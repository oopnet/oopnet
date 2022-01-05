from enum import Enum


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


class HeadlossFormula(str, Enum):
    HW = 'H-W'
    DW = 'D-W'
    CM = 'C-M'

    @classmethod
    def parse(cls, string: str):
        return cls[string.replace('-', '')]


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