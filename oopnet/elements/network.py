from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Union
from dataclasses import dataclass, field
from datetime import datetime

if TYPE_CHECKING:
    from bokeh.plotting import Figure as BokehFigure
    from matplotlib.pyplot import Figure as PyPlotFigure
    from matplotlib.pyplot import Axes
    import pandas as pd

from oopnet.writer.write import write
from oopnet.reader.read import read
from oopnet.plotter.pyplot import Plotsimulation as PyPlot
from oopnet.plotter.bokehplot import Plotsimulation as BokehPlot
from oopnet.simulator.epanet2 import ModelSimulator
from oopnet.elements.water_quality import Reaction
from oopnet.elements.options_and_reporting import Options, Times, Report, Reportparameter, Reportprecision
from oopnet.elements.component_registry import ComponentRegistry, SuperComponentRegistry, NodeRegistry, LinkRegistry
if TYPE_CHECKING:
    from oopnet.elements.system_operation import Energy, Control, Rule, Curve, Pattern
    from oopnet.elements.network_map_tags import Vertex, Label, Backdrop
    from oopnet.report.report import SimulationReport


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
      report: SimulationReport object representing model report settings
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
            startdatetime: Optional[datetime] = None, output: bool = False) -> SimulationReport:
        """Runs an EPANET simulation by calling command line EPANET

        Attributes:
          filename: if thing is an OOPNET network, filename is an option to perform command line EPANET simulations with a specific filename. If filename is a Python None object then a file with a random UUID (universally unique identifier) is generated
          delete: if delete is True the EPANET Input and SimulationReport file is deleted, if False then the simulation results won't be deleted and are stored in a folder named path
          path: Path were to perform the simulations. If path is a Python None object then a tmp-folder is generated

        Returns:
          OOPNET report object

        """
        sim = ModelSimulator(thing=self, filename=filename, delete=delete, path=path, startdatetime=startdatetime,
                             output=output)
        return sim.run()

    def plot(self, fignum: Optional[int] = None, nodes: Optional[pd.Series] = None,
             links: Optional[pd.Series] = None, colorbar: Union[bool, dict] = True,
             colormap: Union[str, dict] = 'viridis', ax: Optional[Axes] = None,
             markersize: float = 8.0, robust: bool = False, vlim=None, nodetruncate=None) -> PyPlotFigure:
        """Plots the Network with simulation results as a network plot with Matplotlib.

        Symbols for Nodes: Junctions are plotted as circles, Reservoirs as diamonds, Tanks as squares.

        Symbols for Links: Pipes are plotted as lines with no markers, Valves are plotted as lines with triangulars in the middle, Pumps are plotted as lines with pentagons

        Args:
          fignum: figure number, where to plot the network
          nodes: Values related to the nodes as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Pressure(rpt)). If nodes is None or specific nodes do not have  values, then the nodes are drawn as black circles
          links: Values related to the links as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Flow(rpt)). If links is None or specific links do not have  values, then the links are drawn as black lines
          colorbar: If True a colorbar is created, if False there is no colorbar in the plot. If one wants to set this setting for nodes and links seperatly, make use of a dictionary with key 'node' for nodes respectively key 'query_link' for links (e.g. colorbar = {'node':True, 'query_link':False} plots a colorbar for nodes but not for links)
          colormap: Colormap defining which colors are used for the simulation results (default is matplotlib's colormap viridis). colormap can either be a string for matplotlib colormaps, a matplotlib.colors.LinearSegmentedColormap object or a matplotlib.colors.ListedColormap object. If one wants to use different colormaps for nodes and links, then make use of a dictionary with key 'node' for nodes respectively key 'query_link' for links (e.g. colormaps = {'node':'jet', 'query_link':'cool'} plots nodes with colormap jet and links using colormap cool)
          ax: Matplotlib Axes object
          markersize: size of markers
          vlim: todo: add description
          robust: If True, 2nd and 98th percentiles are used as limits for the colorbar, else the minima and maxima are used.
          nodetruncate: If True, only junctions for which a value was submitted using the nodes parameter are plotted. If the nodes parameters isn't being used, all junctions are plotted. If not set True, junctions for which no value was submitted using the nodes parameters are plotted in black. This only applies to junctions and not to tanks and reservoirs, which are always plotted.

        Returns:
          Matplotlib's figure handle

        """
        return PyPlot(self, fignum=fignum, nodes=nodes, links=links, colorbar=colorbar, colormap=colormap,
                      ax=ax, markersize=markersize, robust=robust, vlim=vlim, nodetruncate=nodetruncate)

    def bokehplot(self, tools=None, links=None, nodes=None, colormap='jet') -> BokehFigure:
        """Plots the Network with simulation results as a network plot with Bokehplot.

        Symbols for Nodes: Junctions are plotted as circles, Reservoirs as diamonds, Tanks as squares.

        Symbols for Links: Pipes are plotted as lines with no markers, Valves are plotted as lines with triangulars standing on their top in the middle, Pumps are plotted as lines with triangulars standing on an edge

        Args:
          tools: tools used for the Bokeh plot (panning, zooming, ...)
          nodes: Values related to the nodes as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Pressure(rpt)). If nodes is None or specific nodes do not have  values, then the nodes are drawn as black circles
          links: Values related to the links as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Flow(rpt)). f links is None or specific links do not have  values, then the links are drawn as black lines
          colormap: Colormap defining which colors are used for the simulation results (default is matplotlib's colormap jet). colormap can either be a string for matplotlib colormaps, a matplotlib.colors.LinearSegmentedColormap object or a matplotlib.colors.ListedColormap object. If one wants to use different colormaps for nodes and links, then make use of a dictionary with key 'node' for nodes respectively key 'query_link' for links (e.g. colormaps = {'node':'jet', 'query_link':'cool'} plots nodes with colormap jet and links using colormap cool)

        Returns:
          Bokehplot's figure handle

        """
        return BokehPlot(self, tools=tools, links=links, nodes=nodes, colormap=colormap)
