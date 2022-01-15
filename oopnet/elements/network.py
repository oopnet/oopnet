from __future__ import annotations
from copy import deepcopy
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass, field

import networkx as nx

from oopnet.elements.water_quality import Reaction
from oopnet.elements.options_and_reporting import Options, Times, Report, Reportparameter, Reportprecision
if TYPE_CHECKING:
    from oopnet.elements.system_operation import Energy, Control, Rule, Curve, Pattern
    from oopnet.elements.network_components import Node, Junction, Tank, Reservoir, Link, Pump, Pipe, Valve
    from oopnet.elements.network_map_tags import Vertex, Label, Backdrop


@dataclass
class Network:
    """EPANET hydraulic model representation.
    
    An OOPNET Network object contains all the information stored in an EPANET input file. This ranges from physical
    components like Junctions, Tanks or Pipes to non-physical components like Patterns, Curves or Controls. 
    Furthermore, model settings and report parameter settings/precision settings are incorporated as well.

    Attributes:
      title: Contains the networkx graph of the network
      vertices: List of all Vertex objects in the network
      labels: List of all Labels in the network
      backdrop: Contains the Backdrop object of the network
      energies: List of all Energy curves in the network
      controls: List of all Control objects in the network
      rules: List of all Rule objects in the network
      reactions: List of all Reaction objects in the network
      options: Option object representing model options
      times: Time object representing time settings
      report: Report object representing model report settings
      reportparameter: Reportparameter object representing model report parameter settings
      reportprecision: Reportprecision object representing model report parameter precision settings
      graph: Contains the networkx graph of the network
      junctions: List of all Junction objects in the network
      tanks: List of all Tank objects in the network
      reservoirs: List of all Reservoir objects in the network
      pipes: List of all Pipe objects in the network
      pumps: List of all Pump objects in the network
      valves: List of all Valve objects in the network
      curves: List of all Curve objects belonging to the network
      patterns: List of all Pattern objects belonging to the network

    """
    title: Optional[str] = None
    vertices: dict[str, Vertex] = field(default_factory=dict)
    labels: dict[str, Label] = field(default_factory=dict)
    backdrop: Optional[Backdrop] = None
    energies: list[Energy] = field(default_factory=list)
    controls: list[Control] = field(default_factory=list)
    rules: dict[str, Rule] = field(default_factory=dict)
    reactions: Reaction = Reaction
    options: Options = Options()
    times: Times = Times()
    report: Report = Report()
    reportparameter: Reportparameter = Reportparameter()
    reportprecision: Reportprecision = Reportprecision()
    graph: Optional[nx.Graph] = None  # todo: discuss Graph as Network attribute

    junctions: dict[str, Junction] = field(default_factory=dict)
    tanks: dict[str, Tank] = field(default_factory=dict)
    reservoirs: dict[str, Reservoir] = field(default_factory=dict)

    pipes: dict[str, Pipe] = field(default_factory=dict)
    pumps: dict[str, Pump] = field(default_factory=dict)
    valves: dict[str, Valve] = field(default_factory=dict)

    curves: dict[str, Curve] = field(default_factory=dict)
    patterns: dict[str, Pattern] = field(default_factory=dict)

    @property
    def nodes(self) -> dict[str, Node]:
        """Property returning all Junction, Reservoir and Tank objects from the model."""
        return self.junctions | self.reservoirs | self.tanks

    @property
    def links(self) -> dict[str, Link]:
        """Property returning all Pipe, Pump, and Valve objects from the model."""
        return self.pipes | self.pumps | self.valves

    def __deepcopy__(self) -> Network:
        """Produces a deepcopy of the network."""
        network_copy = Network()
        for attr, val in self.__dict__.items():
            setattr(network_copy, attr, deepcopy(val))
        return network_copy
