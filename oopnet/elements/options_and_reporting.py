import datetime
from traits.api import HasStrictTraits, Enum, Either, List, Str, Float, Instance, Int, Any
from .network_components import Node, Pattern, Link


class Options(HasStrictTraits):
    """
    Defines various simulation options.
    """

    __units = Enum('CFS', 'GPM', 'MGD', 'IMGD', 'AFD', 'LPS', 'LPM', 'MLD', 'CMH', 'CMD')
    __headloss = Enum('H-W', 'D-W', 'C-M')
    __hydraulics = Either(None, List('USE', Str), List('SAVE', Str))
    __quality = Any #Either(None, Enum('NONE', 'CHEMICAL', 'AGE'), List('TRACE', Instance(Node)), List('CHEMICAL', Str, Str))
    __viscosity = Either(None, Float)
    __diffusivity = Either(None, Float)
    __specificgravity = Either(None, Float)
    __trials = Either(None, Int)
    __accuracy = Either(None, Float)
    __unbalanced = Either(Enum('STOP', 'CONTINUE'), List('CONTINUE', Int))
    __pattern = Either(None, Int, Instance(Pattern))
    __demandmultiplier = Either(None, Float(1.0))
    __emitterexponent = Either(None, Float(0.5))
    __tolerance = Either(None, Float)
    __map = Either(None, Str)

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, value):
        self.__units = value

    @property
    def headloss(self):
        return self.__headloss

    @headloss.setter
    def headloss(self, value):
        self.__headloss = value

    @property
    def hydraulics(self):
        return self.__hydraulics

    @hydraulics.setter
    def hydraulics(self, value):
        self.__hydraulics = value

    @property
    def quality(self):
        return self.__quality

    @quality.setter
    def quality(self, value):
        self.__quality = value

    @property
    def viscosity(self):
        return self.__viscosity

    @viscosity.setter
    def viscosity(self, value):
        self.__viscosity = value

    @property
    def diffusivity(self):
        return self.__diffusivity

    @diffusivity.setter
    def diffusivity(self, value):
        self.__diffusivity = value

    @property
    def specificgravity(self):
        return self.__specificgravity

    @specificgravity.setter
    def specificgravity(self, value):
        self.__specificgravity = value

    @property
    def trials(self):
        return self.__trials

    @trials.setter
    def trials(self, value):
        self.__trials = value

    @property
    def accuracy(self):
        return self.__accuracy

    @accuracy.setter
    def accuracy(self, value):
        self.__accuracy = value

    @property
    def unbalanced(self):
        return self.__unbalanced

    @unbalanced.setter
    def unbalanced(self, value):
        self.__unbalanced = value

    @property
    def pattern(self):
        return self.__pattern

    @pattern.setter
    def pattern(self, value):
        self.__pattern = value

    @property
    def demandmultiplier(self):
        return self.__demandmultiplier

    @demandmultiplier.setter
    def demandmultiplier(self, value):
        self.__demandmultiplier = value

    @property
    def emitterexponent(self):
        return self.__emitterexponent

    @emitterexponent.setter
    def emitterexponent(self, value):
        self.__emitterexponent = value

    @property
    def tolerance(self):
        return self.__tolerance

    @tolerance.setter
    def tolerance(self, value):
        self.__tolerance = value

    @property
    def map(self):
        return self.__map

    @map.setter
    def map(self, value):
        self.__map = value


class Times(HasStrictTraits):
    """Defines various time step parameters used in the simulation."""
    __duration = Either(Float, Instance(datetime.timedelta))
    __hydraulictimestep = Either(Float, Instance(datetime.timedelta))
    __qualitytimestep = Either(Float, Instance(datetime.timedelta))
    __ruletimestep = Either(Float, Instance(datetime.timedelta))
    __patterntimestep = Either(Float, Instance(datetime.timedelta))
    __patternstart = Either(Float, Instance(datetime.timedelta))
    __reporttimestep = Either(Float, Instance(datetime.timedelta))
    __reportstart = Either(Float, Instance(datetime.timedelta))
    __startclocktime = Instance(datetime.timedelta)
    __statistic = Enum('NONE', 'AVERAGED', 'MINIMUM', 'MAXIMUM', 'RANGE')

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value

    @property
    def hydraulictimestep(self):
        return self.__hydraulictimestep

    @hydraulictimestep.setter
    def hydraulictimestep(self, value):
        self.__hydraulictimestep = value

    @property
    def qualitytimestep(self):
        return self.__qualitytimestep

    @qualitytimestep.setter
    def qualitytimestep(self, value):
        self.__qualitytimestep = value

    @property
    def ruletimestep(self):
        return self.__ruletimestep

    @ruletimestep.setter
    def ruletimestep(self, value):
        self.__ruletimestep = value

    @property
    def patterntimestep(self):
        return self.__patterntimestep

    @patterntimestep.setter
    def patterntimestep(self, value):
        self.__patterntimestep = value

    @property
    def patternstart(self):
        return self.__patternstart

    @patternstart.setter
    def patternstart(self, value):
        self.__patternstart = value

    @property
    def reporttimestep(self):
        return self.__reporttimestep

    @reporttimestep.setter
    def reporttimestep(self, value):
        self.__reporttimestep = value

    @property
    def reportstart(self):
        return self.__reportstart

    @reportstart.setter
    def reportstart(self, value):
        self.__reportstart = value

    @property
    def startclocktime(self):
        return self.__startclocktime

    @startclocktime.setter
    def startclocktime(self, value):
        self.__startclocktime = value

    @property
    def statistic(self):
        return self.__statistic

    @statistic.setter
    def statistic(self, value):
        self.__statistic = value


class Reportparameter(HasStrictTraits):
    """The parameter reporting option is used to identify which quantities are reported on, how many decimal places are
    displayed, and what kind of filtering should be used to limit the output reporting."""
    __elevation = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __demand = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __head = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __pressure = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __quality = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __length = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __diameter = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __flow = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __velocity = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __headloss = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __setting = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __reaction = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))
    __ffactor = Either(None, Enum('YES', 'NO'), List('BELOW', Float), List('ABOVE', Float))

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    def elevation(self, value):
        self.__elevation = value

    @property
    def demand(self):
        return self.__demand

    @demand.setter
    def demand(self, value):
        self.__demand = value

    @property
    def head(self):
        return self.__head

    @head.setter
    def head(self, value):
        self.__head = value

    @property
    def pressure(self):
        return self.__pressure

    @pressure.setter
    def pressure(self, value):
        self.__pressure = value

    @property
    def quality(self):
        return self.__quality

    @quality.setter
    def quality(self, value):
        self.__quality = value

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def diameter(self):
        return self.__diameter

    @diameter.setter
    def diameter(self, value):
        self.__diameter = value

    @property
    def flow(self):
        return self.__flow

    @flow.setter
    def flow(self, value):
        self.__flow = value

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, value):
        self.__velocity = value

    @property
    def headloss(self):
        return self.__headloss

    @headloss.setter
    def headloss(self, value):
        self.__headloss = value

    @property
    def setting(self):
        return self.__setting

    @setting.setter
    def setting(self, value):
        self.__setting = value

    @property
    def reaction(self):
        return self.__reaction

    @reaction.setter
    def reaction(self, value):
        self.__reaction = value

    @property
    def ffactor(self):
        return self.__ffactor

    @ffactor.setter
    def ffactor(self, value):
        self.__ffactor = value


class Reportprecision(HasStrictTraits):
    __elevation = Either(None, Int)
    __demand = Either(None, Int)
    __head = Either(None, Int)
    __pressure = Either(None, Int)
    __quality = Either(None, Int)
    __length = Either(None, Int)
    __diameter = Either(None, Int)
    __flow = Either(None, Int)
    __velocity = Either(None, Int)
    __headloss = Either(None, Int)
    __position = Either(None, Int)
    __setting = Either(None, Int)
    __reaction = Either(None, Int)
    __ffactor = Either(None, Int)

    @property
    def elevation(self):
        return self.__elevation

    @elevation.setter
    def elevation(self, value):
        self.__elevation = value

    @property
    def demand(self):
        return self.__demand

    @demand.setter
    def demand(self, value):
        self.__demand = value

    @property
    def head(self):
        return self.__head

    @head.setter
    def head(self, value):
        self.__head = value

    @property
    def pressure(self):
        return self.__pressure

    @pressure.setter
    def pressure(self, value):
        self.__pressure = value

    @property
    def quality(self):
        return self.__quality

    @quality.setter
    def quality(self, value):
        self.__quality = value

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def diameter(self):
        return self.__diameter

    @diameter.setter
    def diameter(self, value):
        self.__diameter = value

    @property
    def flow(self):
        return self.__flow

    @flow.setter
    def flow(self, value):
        self.__flow = value

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, value):
        self.__velocity = value

    @property
    def headloss(self):
        return self.__headloss

    @headloss.setter
    def headloss(self, value):
        self.__headloss = value

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def setting(self):
        return self.__setting

    @setting.setter
    def setting(self, value):
        self.__setting = value

    @property
    def reaction(self):
        return self.__reaction

    @reaction.setter
    def reaction(self, value):
        self.__reaction = value

    @property
    def ffactor(self):
        return self.__ffactor

    @ffactor.setter
    def ffactor(self, value):
        self.__ffactor = value


class Report(HasStrictTraits):
    """Describes the contents of the output report produced from a simulation."""
    __pagesize = Either(None, Int)
    __file = Either(None, Str)
    __status = Either(None, Enum('YES', 'NO', 'FULL'))
    __summary = Either(None, Enum('YES', 'NO'))
    __energy = Either(None, Enum('YES', 'NO'))
    __nodes = Either(None, Enum('NONE', 'ALL'), Instance(Node), List(Instance(Node)))
    __links = Either(None, Enum('NONE', 'ALL'), Instance(Link), List(Instance(Link)))
    __parameter = Either(None, Enum('YES', 'NO', 'BELOW', 'ABOVE', 'PRECISION'))
    __value = Either(None, Float)


    @property
    def pagesize(self):
        return self.__pagesize

    @pagesize.setter
    def pagesize(self, value):
        self.__pagesize = value

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, value):
        self.__file = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def summary(self):
        return self.__summary

    @summary.setter
    def summary(self, value):
        self.__summary = value

    @property
    def energy(self):
        return self.__energy

    @energy.setter
    def energy(self, value):
        self.__energy = value

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, value):
        self.__nodes = value

    @property
    def links(self):
        return self.__links

    @links.setter
    def links(self, value):
        self.__links = value

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

    def __init__(self):
        super(Report, self).__init__()
        self.pagesize = None
        self.file = None
        self.status = None
        self.summary = None
        self.energy = None
        self.nodes = 'NONE'
        self.links = 'NONE'
        self.parameter = None
        self.value = None
