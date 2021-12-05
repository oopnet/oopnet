from copy import deepcopy
from typing import Optional, List, Dict
from dataclasses import dataclass, field

import networkx as nx

from oopnet.elements.options_and_reporting import Options, Times, Report, Reportparameter, Reportprecision
from oopnet.elements.system_operation import Energy, Control, Rule, Curve, Pattern
from oopnet.elements.water_quality import Reaction


# @dataclass
@dataclass(slots=True)
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
    vertices: Dict[str, 'Vertex'] = field(default_factory=dict)
    labels: Dict[str, 'Label'] = field(default_factory=dict)
    backdrop: Optional['Backdrop'] = None
    energies: List[Energy] = field(default_factory=list)
    controls: List[Control] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)
    reactions: Reaction = Reaction
    options: Options = Options()
    times: Times = Times()
    report: Report = Report()
    reportparameter: Reportparameter = Reportparameter()
    reportprecision: Reportprecision = Reportprecision()
    graph: Optional[nx.Graph] = None

    junctions: Dict[str, 'Junction'] = field(default_factory=dict)
    tanks: Dict[str, 'Tank'] = field(default_factory=dict)
    reservoirs: Dict[str, 'Reservoir'] = field(default_factory=dict)

    pipes: Dict[str, 'Pipe'] = field(default_factory=dict)
    pumps: Dict[str, 'Pump'] = field(default_factory=dict)
    valves: Dict[str, 'Valve'] = field(default_factory=dict)

    curves: Dict[str, Curve] = field(default_factory=dict)
    patterns: Dict[str, Pattern] = field(default_factory=dict)

    @property
    def nodes(self) -> dict:
        """Property returning all Junction, Reservoir and Tank objects from the model."""
        return self.junctions | self.reservoirs | self.tanks

    @property
    def links(self) -> dict:
        """Property returning all Pipe, Pump, and Valve objects from the model."""
        return self.pipes | self.pumps | self.valves

    def __deepcopy__(self):
        # ToDo: Check if elements not inheritated from Network Components are copied in the right way
        network_copy = Network()
        for attr in self.__slots__:
            val = getattr(self, attr)
            setattr(network_copy, attr, deepcopy(val))
        return network_copy
