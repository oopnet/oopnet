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
      _rules: List of all Rule objects in the network
      reactions: List of all Reaction objects in the network
      options: Option object representing model options
      times: Time object representing time settings
      report: Report object representing model report settings
      reportparameter: Reportparameter object representing model report parameter settings
      reportprecision: Reportprecision object representing model report parameter precision settings
      graph: Contains the networkx graph of the network
      _junctions: List of all Junction objects in the network
      _tanks: List of all Tank objects in the network
      _reservoirs: List of all Reservoir objects in the network
      _pipes: List of all Pipe objects in the network
      _pumps: List of all Pump objects in the network
      _valves: List of all Valve objects in the network
      _curves: List of all Curve objects belonging to the network
      _patterns: List of all Pattern objects belonging to the network

    """
    title: Optional[str] = None
    vertices: dict[str, Vertex] = field(default_factory=dict)
    labels: dict[str, Label] = field(default_factory=dict)
    backdrop: Optional[Backdrop] = None
    reactions: Reaction = field(default_factory=Reaction)
    options: Options = field(default_factory=Options)
    times: Times = field(default_factory=Times)
    report: Report = field(default_factory=Report)
    reportparameter: Reportparameter = field(default_factory=Reportparameter)
    reportprecision: Reportprecision = field(default_factory=Reportprecision)
    graph: Optional[nx.Graph] = None  # todo: discuss Graph as Network attribute

    energies: list[Energy] = field(default_factory=list)
    controls: list[Control] = field(default_factory=list)

    _junctions: dict[str, Junction] = field(default_factory=dict)
    _tanks: dict[str, Tank] = field(default_factory=dict)
    _reservoirs: dict[str, Reservoir] = field(default_factory=dict)
    _pipes: dict[str, Pipe] = field(default_factory=dict)
    _pumps: dict[str, Pump] = field(default_factory=dict)
    _valves: dict[str, Valve] = field(default_factory=dict)
    _curves: dict[str, Curve] = field(default_factory=dict)
    _patterns: dict[str, Pattern] = field(default_factory=dict)
    _rules: dict[str, Rule] = field(default_factory=dict)

    # todo: decide to keep or not (currently not in use)
    @property
    def _nodes(self) -> dict[str, Node]:
        """Property returning all Junction, Reservoir and Tank objects from the model."""
        return self._junctions | self._reservoirs | self._tanks

    @property
    def _links(self) -> dict[str, Link]:
        """Property returning all Pipe, Pump, and Valve objects from the model."""
        return self._pipes | self._pumps | self._valves
