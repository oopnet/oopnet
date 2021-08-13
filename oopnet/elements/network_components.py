from traits.api import Str, Float, List, Instance, Either, Enum, ListFloat, Any
from .base import NetworkComponent
from .system_operation import Pattern, Curve


class Node(NetworkComponent):
    """
    Defines base class for all Node like objects in OOPNET (Junction, Reservoir, Tank)
    """
    __xcoordinate = Float
    __ycoordinate = Float
    __elevation = Float
    __initialquality = Float
    __sourcequality = Float
    __sourcetype = Either(None, Enum('CONCEN', 'MASS', 'FLOWPACED', 'SETPOINT'))
    __strength = Float
    __sourcepattern = Either(Instance(Pattern), List(Instance(Pattern)))

    @property
    def xcoordinate(self):
        """
        The horizontal location of the junction on the map, measured in the map's distance units. If left blank the node object will not appear on the network map.
        """
        return self.__xcoordinate

    @xcoordinate.setter
    def xcoordinate(self, value):
        self.__xcoordinate = value

    @property
    def ycoordinate(self):
        """
        The vertical location of the junction on the map, measured in the map's distance units. If left blank the node object will not appear on the network map.
        """
        return self.__ycoordinate

    @ycoordinate.setter
    def ycoordinate(self, value):
        self.__ycoordinate = value

    @property
    def elevation(self):
        """
        The elevation in meters above some common reference of the node. This is a required property. Elevation is used only to compute pressure at the node. For tanks it is a required property and means Elevation above a common datum in meters of the bottom shell of the tank.
        """
        return self.__elevation

    @elevation.setter
    def elevation(self, value):
        self.__elevation = value

    @property
    def initialquality(self):
        """
        Water quality level at the node at the start of the simulation period. Can be left blank if no water quality analysis is being made or if the level is zero.
        """
        return self.__initialquality

    @initialquality.setter
    def initialquality(self, value):
        self.__initialquality = value

    @property
    def sourcequality(self):
        """
        Quality of any water entering the network at this location.
        """
        return self.__sourcequality

    @sourcequality.setter
    def sourcequality(self, value):
        self.__sourcequality = value

    @property
    def sourcetype(self):
        """
        Source type (CONCEN, MASS, FLOWPACED, or SETPOINT)
        """
        return self.__sourcetype

    @sourcetype.setter
    def sourcetype(self, value):
        self.__sourcetype = value

    @property
    def strength(self):
        """
        Baseline source strength
        """
        return self.__strength

    @strength.setter
    def strength(self, value):
        self.__strength = value

    @property
    def sourcepattern(self):
        """
        Time Pattern object of source
        """
        return self.__sourcepattern

    @sourcepattern.setter
    def sourcepattern(self, value):
        self.__sourcepattern = value

    def __init__(self,
                 id='',
                 comment=None,
                 xcoordinate=0.0,
                 ycoordinate=0.0,
                 elevation=0.0,
                 initialquality=0.0,
                 sourcequality=0.0,
                 sourcetype=None,
                 strength=0.0,
                 sourcepattern=None
                 ):
        # super(Node, self).__init__()
        self.id = id
        self.comment = comment
        self.xcoordinate = xcoordinate
        self.ycoordinate = ycoordinate
        self.elevation = elevation
        self.initialquality = initialquality
        self.sourcequality = sourcequality
        self.sourcetype = sourcetype
        self.strength = strength
        self.sourcepattern = sourcepattern


class Link(NetworkComponent):
    """
    Defines base class for all Link like objects in OOPNET (Pipe, Pump, Valve)
    """
    __startnode = Instance(Node)
    __endnode = Instance(Node)
    __initialstatus = Either(None, Enum('OPEN', 'CLOSED', 'ACTIVE', 'CV'), Float)
    __status = Enum('OPEN', 'CLOSED', 'ACTIVE', 'CV')
    __setting = Any  # ToDo: Rethink if any is correct for setting attribute

    @property
    def startnode(self):
        """
        Node-object at the start of the Link
        """
        return self.__startnode

    @startnode.setter
    def startnode(self, value):
        self.__startnode = value

    @property
    def endnode(self):
        """
        Node-object at the end of the Link
        """
        return self.__endnode

    @endnode.setter
    def endnode(self, value):
        self.__endnode = value

    @property
    def initialstatus(self):
        """
        Status at the beginning of the simulation of the Link (OPEN, CLOSED, CV or ACTIVE)
        """
        return self.__initialstatus

    @initialstatus.setter
    def initialstatus(self, value):
        self.__initialstatus = value

    @property
    def status(self):
        """
        Current status of the Link (OPEN, CLOSED, CV or ACTIVE)
        """
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def setting(self):
        """
        SETTING: Roughness for pipes, speed for pumps, pressure/flow setting for valves
        """
        # ToDo: rethink if this is necessary
        return self.__setting

    @setting.setter
    def setting(self, value):
        self.__setting = value


class Junction(Node):
    """
    Defines Junction nodes contained in the network.
    """

    __emittercoefficient = Float
    __demandpattern = Either(Instance(Pattern), List(Instance(Pattern)))
    __demand = Either(Float, ListFloat)

    @property
    def emittercoefficient(self):
        """
        Discharge coefficient for emitter (sprinkler or nozzle) placed at junction. The coefficient represents the flow (in current flow units) that occurs at a pressure drop of 1 meter. Leave blank if no emitter is present. See the Emitters topic in the Epanet Manual Section 3.1 for more details.
        """
        return self.__emittercoefficient

    @emittercoefficient.setter
    def emittercoefficient(self, value):
        self.__emittercoefficient = value

    @property
    def demandpattern(self):
        """
        Pattern object used to characterize time variation in demand for the main category of consumer at the junction. The pattern provides multipliers that are applied to the Base Demand to determine actual demand in a given time period.
        """
        return self.__demandpattern

    @demandpattern.setter
    def demandpattern(self, value):
        self.__demandpattern = value

    @property
    def demand(self):
        """
        The average or nominal demand for water by the main category of consumer at the junction, as measured in the current flow units. A negative value is used to indicate an external source of flow into the junction. If left blank then demand is assumed to be zero.
        """
        return self.__demand

    @demand.setter
    def demand(self, value):
        self.__demand = value

    def __init__(self,
                 id='',
                 comment=None,
                 xcoordinate=0.0,
                 ycoordinate=0.0,
                 elevation=0.0,
                 initialquality=0.0,
                 sourcequality=0.0,
                 sourcetype=None,
                 strength=0.0,
                 sourcepattern=None,
                 emittercoefficient=0.0,
                 demandpattern=None,
                 demand=0.0
                 ):
        # super(Node, self).__init__()
        self.id = id
        self.comment = comment
        self.xcoordinate = xcoordinate
        self.ycoordinate = ycoordinate
        self.elevation = elevation
        self.initialquality = initialquality
        self.sourcequality = sourcequality
        self.sourcetype = sourcetype
        self.strength = strength
        self.sourcepattern = sourcepattern
        self.emittercoefficient = emittercoefficient
        self.demandpattern = demandpattern
        self.demand = demand

class Reservoir(Node):
    """
    Defines all reservoir nodes contained in the network.
    """

    __head = Either(None, Float, ListFloat)
    __headpattern = Either(None, Instance(Pattern), List(Instance(Pattern)))
    __mixingmodel = Enum('MIXED', '2COMP', 'FIFO', 'LIFO')


    @property
    def head(self):
        """
        The hydraulic head (elevation + pressure head) of water in the reservoir in meters. This is a required property.
        """
        return self.__head

    @head.setter
    def head(self, value):
        self.__head = value

    @property
    def headpattern(self):
        """
        Pattern object used to model time variation in the reservoir's head. Leave blank if none applies. This property is useful if the reservoir represents a tie-in to another system whose pressure varies with time.
        """
        return self.__headpattern

    @headpattern.setter
    def headpattern(self, value):
        self.__headpattern = value


    @property
    def mixingmodel(self):
        """
        The type of water quality mixing that occurs within the tank. The choices include

        * MIXED (fully mixed),

        * 2COMP (two-compartment mixing),

        * FIFO (first-in-first-out plug flow),

        * LIFO (last-in-first-out plug flow).
        """
        return self.__mixingmodel


    @mixingmodel.setter
    def mixingmodel(self, value):
        self.__mixingmodel = value


class Tank(Node):
    """
    Defines all tank nodes contained in the network.
    """

    __initlevel = Float
    __minlevel = Float
    __maxlevel = Float
    __diam = Float
    __minvolume = Float
    __volumecurve = Instance(Curve)
    __mixingmodel = Enum('MIXED', '2COMP', 'FIFO', 'LIFO')
    __compartmentvolume = Float
    __reactiontank = Float


    @property
    def initlevel(self):
        """
        Height in meters of the water surface above the bottom elevation of the tank at the start of the simulation. This is a required property.
        """
        return self.__initlevel

    @initlevel.setter
    def initlevel(self, value):
        self.__initlevel = value

    @property
    def minlevel(self):
        """
        Minimum height in meters of the water surface above the bottom elevation that will be maintained. The tank will not be allowed to drop below this level. This is a required property.
        """
        return self.__minlevel

    @minlevel.setter
    def minlevel(self, value):
        self.__minlevel = value

    @property
    def maxlevel(self):
        """
        Maximum height in meters of the water surface above the bottom elevation that will be maintained. The tank will not be allowed to rise above this level. This is a required property.
        """
        return self.__maxlevel

    @maxlevel.setter
    def maxlevel(self, value):
        self.__maxlevel = value

    @property
    def diam(self):
        """
        The diameter of the tank in meters. For cylindrical tanks this is the actual diameter. For square or rectangular tanks it can be an equivalent diameter equal to 1.128 times the square root of the cross-sectional area. For tanks whose geometry will be described by a curve (see below) it can be set to any value. This is a required property.
        """
        return self.__diam

    @diam.setter
    def diam(self, value):
        self.__diam = value

    @property
    def minvolume(self):
        """
        The volume of water in the tank when it is at its minimum level, in cubic meter. This is an optional property, useful mainly for describing the bottom geometry of non-cylindrical tanks where a full volume versus depth curve will not be supplied (see below).
        """
        return self.__minvolume

    @minvolume.setter
    def minvolume(self, value):
        self.__minvolume = value

    @property
    def volumecurve(self):
        """
        Curve object used to describe the relation between tank volume and water level. If no value is supplied then the tank is assumed to be cylindrical.
        """
        return self.__volumecurve

    @volumecurve.setter
    def volumecurve(self, value):
        self.__volumecurve = value

    @property
    def mixingmodel(self):
        """
        The type of water quality mixing that occurs within the tank. The choices include

        * MIXED (fully mixed),

        * 2COMP (two-compartment mixing),

        * FIFO (first-in-first-out plug flow),

        * LIFO (last-in-first-out plug flow).
        """
        return self.__mixingmodel

    @mixingmodel.setter
    def mixingmodel(self, value):
        self.__mixingmodel = value

    @property
    def compartmentvolume(self):
        """

        """
        return self.__compartmentvolume

    @compartmentvolume.setter
    def compartmentvolume(self, value):
        self.__compartmentvolume = value

    @property
    def reactiontank(self):
        """
        The bulk reaction coefficient for chemical reactions in the tank. Time units are 1/days. Use a positive value for growth reactions and a negative value for decay. Leave blank if the Global Bulk reaction coefficient specified in the project's Reactions Options will apply. See Water Quality Reactions in the Epanet manual Section 3.4 for more information.

        """
        return self.__reactiontank

    @reactiontank.setter
    def reactiontank(self, value):
        self.__reactiontank = value

class Pipe(Link):
    """
    Defines all pipe links contained in the network.
    """

    __length = Float
    __diameter = Float
    __roughness = Float
    __minorloss = Float
    __reactionbulk = Float
    __reactionwall = Float

    @property
    def length(self):
        """
        The actual length of the pipe in meters. This is a required property.
        """
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def diameter(self):
        """
        The pipe diameter in mm. This is a required property.
        """
        return self.__diameter

    @diameter.setter
    def diameter(self, value):
        self.__diameter = value

    @property
    def roughness(self):
        """
        The roughness coefficient of the pipe. It is unitless for Hazen-Williams or Chezy-Manning roughness and has units of mm for Darcy-Weisbach roughness. This is a required property.
        """
        return self.__roughness

    @roughness.setter
    def roughness(self, value):
        self.__roughness = value

    @property
    def minorloss(self):
        """
        Unitless minor loss coefficient associated with bends, fittings, etc. Assumed 0 if left blank.
        """
        return self.__minorloss

    @minorloss.setter
    def minorloss(self, value):
        self.__minorloss = value

    @property
    def reactionbulk(self):
        """
        The bulk reaction coefficient for the pipe. Time units are 1/days. Use a positive value for growth and a negative value for decay. Leave blank if the Global Bulk reaction coefficient from the project's Reaction Options will apply. See Water Quality Reactions in the Epanet Manual Section 3.4 for more information.
        """
        return self.__reactionbulk

    @reactionbulk.setter
    def reactionbulk(self, value):
        self.__reactionbulk = value

    @property
    def reactionwall(self):
        """
        The wall reaction coefficient for the pipe. Time units are 1/days. Use a positive value for growth and a negative value for decay. Leave blank if the Global Wall reaction coefficient from the project's Reactions Options will apply. See Water Quality Reactions in the Epanet Manual Section 3.4 for more information.
        """
        return self.__reactionwall

    @reactionwall.setter
    def reactionwall(self, value):
        self.__reactionwall = value




class Pump(Link):
    """
    Defines all pump links contained in the network.
    """

    __keyword = Enum('POWER', 'HEAD', 'SPEED', 'PATTERN')
    __value = Any
    __status = Either(None, Enum('OPEN', 'CLOSED', 'ACTIVE'), Float)

    @property
    def keyword(self):
        """
        a. Keywords consists of:

        * POWER - power value for constant energy pump, hp (kW)

        * HEAD - ID of curve that describes head versus flow for the pump

        * SPEED - relative speed setting (normal speed is 1.0, 0 means pump is off)

        * PATTERN - ID of time pattern that describes how speed setting varies with time

        b. Either POWER or HEAD must be supplied for each pump. The other keywords are optional.
        """
        return self.__keyword

    @keyword.setter
    def keyword(self, value):
        self.__keyword = value

    @property
    def value(self):
        """
        Value according to the keyword property
        """
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Valve(Link):
    """
    Defines all control valve links contained in the network
    """

    __valvetype = Str
    __diameter = Float
    __minorloss = Float

    @property
    def valvetype(self):
        """
        A required parameter that describes the valve's operational setting (PRV, PSV, PBV, FCV, TCV, GPV).
        """
        return self.__valvetype

    @valvetype.setter
    def valvetype(self, value):
        self.__valvetype = value

    @property
    def diameter(self):
        """
        The valve diameter in mm. This is a required property.
        """
        return self.__diameter

    @diameter.setter
    def diameter(self, value):
        self.__diameter = value

    @property
    def minorloss(self):
        """
        Unitless minor loss coefficient that applies when the valve is completely opened. Assumed 0 if left blank.

        """
        return self.__minorloss

    @minorloss.setter
    def minorloss(self, value):
        self.__minorloss = value


class PRV(Valve):
    # ToDo: Implement PRV (Pressure Reducing Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


class TCV(Valve):
    # ToDo: Implement TCV (Throttle Control Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


class PSV(Valve):
    # ToDo: Implement PSV (Pressure Sustaining Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


class GPV(Valve):
    # ToDo: Implement GPV (General Purpose Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


class PBV(Valve):
    # ToDo: Implement PBV (Pressure Breaker Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass


class FCV(Valve):
    # ToDo: Implement FCV (Flow Control Valve)
    """
    .. warning::

        Not implemented yet

    """
    pass
