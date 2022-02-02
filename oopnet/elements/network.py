from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass, field
from datetime import datetime

import networkx as nx

from oopnet.writer.write import write
from oopnet.reader.read import read
from oopnet.simulator.epanet2 import ModelSimulator
from oopnet.elements.water_quality import Reaction
from oopnet.elements.options_and_reporting import Options, Times, Report, Reportparameter, Reportprecision
from oopnet.elements.component_registry import ComponentRegistry, SuperComponentRegistry, NodeRegistry, LinkRegistry
if TYPE_CHECKING:
    from oopnet.elements.system_operation import Energy, Control, Rule, Curve, Pattern
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

    _nodes: SuperComponentRegistry = field(default_factory=NodeRegistry)
    _links: SuperComponentRegistry = field(default_factory=LinkRegistry)
    _curves: dict[str, Curve] = field(default_factory=ComponentRegistry)
    _patterns: dict[str, Pattern] = field(default_factory=ComponentRegistry)
    _rules: dict[str, Rule] = field(default_factory=ComponentRegistry)

    @classmethod
    def read(cls, filename=Optional[str], content=Optional[str]):
        """Reads an EPANET input file.

        Args:
          filename: filename of the EPANET input file

        """
        network = cls()
        return read(network=network, filename=filename, content=content)

    def write(self, filename):
        """Converts the Network to an EPANET input file and saves it with the desired filename.

        Args:
          filename: desired filename/path were the user wants to store the file

        Returns:
          0 if successful

        """
        return write(self, filename)

    def run(self, filename: Optional[str] = None, delete: bool = True, path: Optional[str] = None,
            startdatetime: Optional[datetime] = None, output: bool = False):
        """Runs an EPANET simulation by calling command line EPANET

        Attributes:
          filename: if thing is an OOPNET network, filename is an option to perform command line EPANET simulations with a specific filename. If filename is a Python None object then a file with a random UUID (universally unique identifier) is generated
          delete: if delete is True the EPANET Input and Report file is deleted, if False then the simulation results won't be deleted and are stored in a folder named path
          path: Path were to perform the simulations. If path is a Python None object then a tmp-folder is generated

        Returns:
          OOPNET report object

        """
        sim = ModelSimulator(thing=self, filename=filename, delete=delete, path=path, startdatetime=startdatetime,
                             output=output)
        return sim.run()
