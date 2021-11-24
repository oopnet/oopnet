from .network_components import *
from .system_operation import *
from .options_and_reporting import *
from .network_map_tags import *
from .water_quality import *
import networkx as nx
from copy import deepcopy
from typing import List
from sortedcontainers import SortedKeyList
from dataclasses import dataclass, field


class ComponentList(SortedKeyList):
    """Class for storing NetworkComponent objects."""
    def __init__(self, data=None, key=lambda x: x.id):
        if data is None:
            data = []
        super().__init__(data, key=key)

    def append(self, value):
        self.add(value)

    def binary_search(self, id):
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
    title: str = ''
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
        return self.junctions + self.reservoirs + self.tanks

    @property
    def links(self) -> list:
        return self.pipes + self.pumps + self.valves

    def __deepcopy__(self):
        # ToDo: Check if elements not inheritated from Network Components are copied in the right way
        network_copy = Network()
        for k, v in list(self.__dict__.items()):
            setattr(network_copy, k, deepcopy(v))
        return network_copy
