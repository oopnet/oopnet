from copy import deepcopy
from typing import Iterable, Callable, Optional, List, Union
from dataclasses import dataclass, field

from sortedcontainers import SortedKeyList
import networkx as nx

from .base import NetworkComponent
from .network_components import Junction, Tank, Reservoir, Pipe, Pump, Valve, Node, Link
from .network_map_tags import Vertex, Label, Backdrop
from .options_and_reporting import Options, Times, Report, Reportparameter, Reportprecision
from .system_operation import Energy, Control, Rule, Curve, Pattern
from .water_quality import Reaction


class ComponentList(SortedKeyList):
    """Class for storing NetworkComponent objects.

    Attributes:
      data: Iterable containing NetworkComponents to be stored
      key: Callable to be used for sorting the objects

    """
    def __init__(self, data: Optional[Iterable[NetworkComponent]] = None, key: Callable = lambda x: x.id):
        if data is None:
            data = []
        super().__init__(data, key=key)

    def append(self, value: NetworkComponent):
        """Compatibility method for adding a NetworkComponent to a ComponentList.

        Args:
          value: NetworkComponent to add to the ComponentList

        """
        self.add(value)

    def binary_search(self, id: str) -> Union[Junction, Tank, Reservoir, Pipe, Pump, Valve, Pattern, Curve, Rule,
                                              Node, Link]:
        """Lookup method for getting a NetworkComponent by its ID.

        Args:
          id: Queried NetworkComponent's ID

        Returns:
            NetworkComponent with submitted ID

        """
        first = 0
        last = len(self) - 1
        index = -1
        while (first <= last) and (index == -1):
            mid = (first + last) // 2
            if self[mid].id == id:
                index = mid
            elif id < self[mid].id:
                last = mid - 1
            else:
                first = mid + 1
        if self[index].id != id:
            raise KeyError(f'No component with the ID "{id}" found in network.')
        return self[index]


@dataclass
class Network:
    """EPANET hydraulic model representation.

    Attributes:
      title: Contains the networkx graph of the network
      vertices: List of all Vertex-objects in the network
      labels: List of all Labels in the network
      backdrop: Contains the Backdrop-Object of the network
      energies: List of all Energy curves in the network
      controls: List of all Control-objects in the network
      rules: List of all Rule-objects in the network
      reactions: List of all Reaction-objects in the network
      options: Option-object representing model options
      times: Time-object representing time settings
      report: Report-object representing model report settings
      reportparameter: Reportparameter-object representing model report parameter settings
      reportprecision: Reportprecision-object representing model report parameter precision settings
      graph: Contains the networkx graph of the network
      junctions: List of all Junction-objects in the network
      tanks: List of all Tank-objects in the network
      reservoirs: List of all Reservoir-objects in the network
      pipes: List of all Pipe-objects in the network
      pumps: List of all Pump-objects in the network
      valves: List of all Valve-objects in the network
      curves: List of all Curve-objects belonging to the network
      patterns: List of all Pattern-objects belonging to the network

    """
    title: Optional[str] = None
    vertices: ComponentList[Vertex] = field(default_factory=ComponentList)
    labels: ComponentList[Label] = field(default_factory=ComponentList)
    backdrop: Optional[Backdrop] = None
    energies: List[Energy] = field(default_factory=list)
    controls: ComponentList[Control] = field(default_factory=ComponentList)
    rules: ComponentList[Rule] = field(default_factory=ComponentList)
    reactions: Reaction = Reaction
    options: Options = Options()
    times: Times = Times()
    report: Report = Report()
    reportparameter: Reportparameter = Reportparameter()
    reportprecision: Reportprecision = Reportprecision()
    graph: Optional[nx.Graph] = None

    junctions: ComponentList[Junction] = field(default_factory=ComponentList)
    tanks: ComponentList[Tank] = field(default_factory=ComponentList)
    reservoirs: ComponentList[Reservoir] = field(default_factory=ComponentList)

    pipes: ComponentList[Pipe] = field(default_factory=ComponentList)
    pumps: ComponentList[Pump] = field(default_factory=ComponentList)
    valves: ComponentList[Valve] = field(default_factory=ComponentList)

    curves: ComponentList[Curve] = field(default_factory=ComponentList)
    patterns: ComponentList[Pattern] = field(default_factory=ComponentList)

    @property
    def nodes(self) -> ComponentList:
        """Property returning all Junction, Reservoir and Tank objects from the model."""
        return self.junctions + self.reservoirs + self.tanks

    @property
    def links(self) -> ComponentList:
        """Property returning all Pipe, Pump, and Valve objects from the model."""
        return self.pipes + self.pumps + self.valves

    def __deepcopy__(self):
        # ToDo: Check if elements not inheritated from Network Components are copied in the right way
        network_copy = Network()
        for k, v in list(self.__dict__.items()):
            setattr(network_copy, k, deepcopy(v))
        return network_copy
