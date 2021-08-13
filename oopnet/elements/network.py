from traits.api import Dict
from .network_components import *
from .system_operation import *
from .options_and_reporting import *
from .network_map_tags import *
from .water_quality import *
import networkx as nx
from copy import deepcopy


class Network(HasStrictTraits):

    # ToDo: Decide if a single instance of a object makes sense or if the
    # properties should always contain lists of e.g. reservoirs or junctions
    __title = Str
    __junctions = Either(Instance(Junction), List(Instance(Junction)))
    __reservoirs = Either(Instance(Reservoir), List(Instance(Reservoir)))
    __tanks = Either(Instance(Tank), List(Instance(Tank)))
    __pipes = Either(Instance(Pipe), List(Instance(Pipe)))
    __pumps = Either(Instance(Pump), List(Instance(Pump)))
    __valves = Either(Instance(Valve), List(Instance(Valve)))
    __patterns = Either(Instance(Pattern), List(Instance(Pattern)))
    __vertices = Either(Instance(Vertex), List(Instance(Vertex)))
    __labels = Either(Instance(Label), List(Instance(Label)))
    __backdrop = Instance(Backdrop)
    __curves = Either(Instance(Curve), List(Instance(Curve)))
    __energies = Either(Instance(Energy), List(Instance(Energy)))
    __controls = Either(Instance(Control), List(Instance(Control)))
    __rules = Either(Instance(Rule), List(Instance(Rule)))
    __reactions = Either(Instance(Reaction), List(Instance(Reaction)))
    __options = Instance(Options)
    __times = Instance(Times)
    __report = Instance(Report)
    __reportparameter = Instance(Reportparameter)
    __reportprecision = Instance(Reportprecision)
    __networkhash = Dict
    __graph = Instance(nx.Graph)

    @property
    def graph(self):
        """
        Contains the networkx graph of the network
        """
        return self.__graph

    @graph.setter
    def graph(self, value):
        self.__graph = value

    @property
    def patterns(self):
        """
        List of all Pattern-objects belonging to the network
        """
        return self.__patterns

    @patterns.setter
    def patterns(self, value):
        self.__patterns = value

    @property
    def title(self):
        """
        Contains the Title of the EPANET Input file
        """
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def junctions(self):
        """
        List of all Junction-objects in the network
        """
        return self.__junctions

    @junctions.setter
    def junctions(self, value):
        self.__junctions = value

    @property
    def reservoirs(self):
        """
        List of all Reservoir-objects in the network
        """
        return self.__reservoirs

    @reservoirs.setter
    def reservoirs(self, value):
        self.__reservoirs = value

    @property
    def tanks(self):
        """
        List of all Tank-objects in the network
        """
        return self.__tanks

    @tanks.setter
    def tanks(self, value):
        self.__tanks = value

    @property
    def pipes(self):
        """
        List of all Pipe-objects in the network
        """
        return self.__pipes

    @pipes.setter
    def pipes(self, value):
        self.__pipes = value

    @property
    def pumps(self):
        """
        List of all Pump-objects in the network
        """
        return self.__pumps

    @pumps.setter
    def pumps(self, value):
        self.__pumps = value

    @property
    def valves(self):
        """
        List of all Valve-objects in the network
        """
        return self.__valves

    @valves.setter
    def valves(self, value):
        self.__valves = value

    @property
    def vertices(self):
        """
        List of all Vertex-objects in the network
        """
        return self.__vertices

    @vertices.setter
    def vertices(self, value):
        self.__vertices = value

    @property
    def labels(self):
        """
        List of all Labels in the network
        """
        return self.__labels

    @labels.setter
    def labels(self, value):
        self.__labels = value

    @property
    def backdrop(self):
        """
        Contains the Backdrop-Object of the network
        """
        return self.__backdrop

    @backdrop.setter
    def backdrop(self, value):
        self.__backdrop = value

    @property
    def networkhash(self):
        """
        Dictionary linking to different types objects in the network:

                ``node``
                    Dictionary with Node id's as keys and instances of the corresponding Node-objects as values
                ``link``
                    Dictionary with Link id's as keys and instances of the corresponding Link-objects as values
                ``pattern``
                    Dictionary with Pattern id's as keys and instances of the corresponding Pattern-objects as values
                ``curve``
                     Dictionary with Curve id's as keys and instances of the corresponding Curve-objects as values
        """
        return self.__networkhash

    @networkhash.setter
    def networkhash(self, value):
        self.__networkhash = value

    @property
    def curves(self):
        """
        List of all Curve-objects belonging to the network
        """
        return self.__curves

    @curves.setter
    def curves(self, value):
        self.__curves = value

    @property
    def energies(self):
        """
        List of all Energy curves in the network
        """
        return self.__energies

    @energies.setter
    def energies(self, value):
        self.__energies = value

    @property
    def controls(self):
        """
        List of all Control-objects in the network
        """
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value

    @property
    def rules(self):
        """
        List of all Rule-objects in the network
        """
        return self.__rules

    @rules.setter
    def rules(self, value):
        self.__rules = value

    @property
    def reactions(self):
        """
        List of all Reaction-objects in the network
        """
        return self.__reactions

    @reactions.setter
    def reactions(self, value):
        self.__reactions = value

    @property
    def options(self):
        """
        Property containing the Option-object
        """
        return self.__options

    @options.setter
    def options(self, value):
        self.__options = value

    @property
    def times(self):
        """
        Property containing the Time-object
        """
        return self.__times

    @times.setter
    def times(self, value):
        self.__times = value

    @property
    def report(self):
        """
        Property containing the Report-object
        """
        return self.__report

    @report.setter
    def report(self, value):
        self.__report = value

    @property
    def reportparameter(self):
        """
        Property containing the Reportparameter-object
        """
        return self.__reportparameter

    @reportparameter.setter
    def reportparameter(self, value):
        self.__reportparameter = value

    @property
    def reportprecision(self):
        """
        Property containing the Reportprecision-object
        """
        return self.__reportprecision

    @reportprecision.setter
    def reportprecision(self, value):
        self.__reportprecision = value

    def __init__(self):
        super(Network, self).__init__()
        self.networkhash = dict()
        self.networkhash['node'] = dict()
        self.networkhash['link'] = dict()
        self.networkhash['pattern'] = dict()
        self.networkhash['curve'] = dict()

    def __deepcopy__(self):
        # ToDo: Check if elements not inheritated from Network Components are copied in the right way
        cls = self.__class__
        result = cls.__new__(cls)
        for k, v in list(self.__dict__.items()):
            setattr(result, k, deepcopy(v))
        return result
