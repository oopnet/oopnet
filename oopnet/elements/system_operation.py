import datetime
from traits.api import HasStrictTraits, List, ListFloat, Enum, Instance, Either, Float
from .base import NetworkComponent


class Curve(NetworkComponent):
    """
    Defines data curves and their X,Y points.
    """

    __xvalues = ListFloat
    __yvalues = ListFloat

    @property
    def xvalues(self):
        return self.__xvalues

    @xvalues.setter
    def xvalues(self, value):
        self.__xvalues = value

    @property
    def yvalues(self):
        return self.__yvalues

    @yvalues.setter
    def yvalues(self, value):
        self.__yvalues = value


class Pattern(NetworkComponent):
    """
    Defines time patterns.
    """

    __multipliers = List

    @property
    def multipliers(self):
        return self.__multipliers

    @multipliers.setter
    def multipliers(self, value):
        self.__multipliers = value


class Energy(HasStrictTraits):
    """
    Defines parameters used to compute pumping energy and cost.
    """

    __keyword = Enum('GLOBAL', 'PUMP', 'DEMAND CHARGE')
    __pumpid = Instance(NetworkComponent)  # ToDo: pipeid self referencing on pump class instead of NetworkComponent
    __parameter = Either(None, Enum('PRICE', 'EFFIC', 'PATTERN', 'EFFICIENCY'))
    __value = Either(Float, Instance(Pattern), Instance(Curve))

    @property
    def keyword(self):
        return self.__keyword

    @keyword.setter
    def keyword(self, value):
        self.__keyword = value

    @property
    def pumpid(self):
        return self.__pumpid

    @pumpid.setter
    def pumpid(self, value):
        self.__pumpid = value

    @property
    def parameter(self):
        return self.__parameter

    @parameter.setter
    def parameter(self, value):
        self.__parameter = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Condition(HasStrictTraits):
    """A condition clause in a rule-based control"""
    # ToDo: object attribute should be either instance of Node or Link instead of Network Component
    __object = Instance(NetworkComponent)
    # __object = Either(Instance(Node), Instance(Link))
    __logical = Either('IF', 'AND', 'OR', 'THEN', 'ELSE')
    __attribute = Enum('DEMAND', 'HEAD', 'PRESSURE', 'LEVEL', 'FILLTIME', 'DRAINTIME', 'FLOW', 'STATUS', 'SETTING',
                       'TIME', 'CLOCKTIME')
    __relation = Enum('=', '<>', '<', '>', '<=', '>=', 'IS', 'NOT', 'BELOW', 'ABOVE')
    __value = Either(Float, Enum('OPEN', 'CLOSED'), Instance(datetime.datetime), Instance(datetime.timedelta))

    @property
    def object(self):
        return self.__object

    @object.setter
    def object(self, value):
        self.__object = value

    @property
    def attribute(self):
        return self.__attribute

    @attribute.setter
    def attribute(self, value):
        self.__attribute = value

    @property
    def relation(self):
        return self.__relation

    @relation.setter
    def relation(self, value):
        self.__relation = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def logical(self):
        return self.__logical

    @logical.setter
    def logical(self, value):
        self.__logical = value


class Action(HasStrictTraits):
    """An action clause in a rule-based control"""
    # ToDo: object attribute should be either instance of Node or Link instead of Network Component
    __object = Either(NetworkComponent, 'SYSTEM')
    # __object = Either(Instance(Node), Instance(Link), 'SYSTEM')
    __value = Either(Float, Enum('OPEN', 'CLOSED'))

    @property
    def object(self):
        return self.__object

    @object.setter
    def object(self, value):
        self.__object = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Rule(NetworkComponent):
    """Defines rule-based controls that modify links based on a combination of conditions."""
    __condition = Either(Instance(Condition), List(Instance(Condition)))
    __priority = Float

    @property
    def condition(self):
        return self.__condition

    @condition.setter
    def condition(self, value):
        self.__condition = value

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        self.__priority = value


class Controlcondition(HasStrictTraits):

    # ToDo: object attribute should be either instance of Node instead of Network Component
    __object = Instance(NetworkComponent)
    # __object = Instance(Node)
    __relation = Enum('ABOVE', 'BELOW')
    __value = Float
    __time = Either(Float, Instance(datetime.timedelta))
    __clocktime = Instance(datetime.datetime)

    @property
    def object(self):
        return self.__object

    @object.setter
    def object(self, value):
        self.__object = value

    @property
    def relation(self):
        return self.__relation

    @relation.setter
    def relation(self, value):
        self.__relation = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        self.__time = value

    @property
    def clocktime(self):
        return self.__clocktime

    @clocktime.setter
    def clocktime(self, value):
        self.__clocktime = value


class Control(HasStrictTraits):

    """Defines simple controls that modifiy links based on a single condition."""
    __action = Instance(Action)
    __condition = Instance(Controlcondition)

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value

    @property
    def condition(self):
        return self.__condition

    @condition.setter
    def condition(self, value):
        self.__condition = value
