import datetime
from typing import Optional, Union, Type, Callable
import logging

import pandas as pd
from xarray import DataArray

from oopnet.simulators.binaryfile_reader import BinaryFileReader
from oopnet.simulators.reportfile_reader import ReportFileReader

logger = logging.getLogger(__name__)


# todo: add documentation
class SimulationReport:
    """Class for storing stimulation results.

    Attributes:
        nodes: Node results
        links: Link results
    """

    nodes: DataArray
    links: DataArray

    def __init__(
        self,
        filename: Union[str, None] = None,
        startdatetime: Optional[datetime.datetime] = None,
        reader: Union[
            Type[BinaryFileReader], Type[ReportFileReader], None
        ] = ReportFileReader,
        report: Union[tuple[Type[DataArray]], None] = None,
    ):
        """SimulationReport init method.

        Args:
            filename: name of EPANET input file be simulated
            startdatetime:
            reader: specifies whether the report or the binary file created by EPANET are read

        """
        if report is None:
            logger.debug("Creating report.")
            self.nodes, self.links = reader(filename, startdatetime)
        else:
            self.nodes, self.links = report

    @staticmethod
    def _get(
        array: DataArray,
        var: str,
        unit: Optional[str] = None,
        calc: Optional[Callable] = None,
    ):
        data = array.sel(vars=var).to_pandas().sort_index()
        if calc:
            data = calc(data)
        data.name = f"{var} ({unit})" if unit else var
        return data

    @staticmethod
    def _get_element_info(array: DataArray, id: str) -> pd.Series:
        data = array.sel(id=id).to_pandas()
        data.name = id
        return data

    @property
    def elevation(self) -> Union[pd.Series, pd.DataFrame]:
        """Elevations from the simulation report object.

        Returns:
          Pandas Series containing the elevations of the Nodes

        """
        return self._get(self.nodes, "Elevation", "m")

    @property
    def demand(self) -> Union[pd.Series, pd.DataFrame]:
        """Demands from the simulation report object.

        Returns:
          Pandas Series containing the demands of the Nodes

        """
        return self._get(self.nodes, "Demand", "l/s")

    @property
    def consumption(self) -> Union[pd.Series, pd.DataFrame]:
        """Consumptions from the simulation report object.

        Returns:
          Pandas Series containing the consumptions at the Nodes

        """
        var, unit = "Consumption", "l/s"
        try:
            c = self._get(self.nodes, var, unit)
        except KeyError:
            c = self.demand
            c.name = f"{var} ({unit})" if unit else var
        return c

    @property
    def head(self) -> Union[pd.Series, pd.DataFrame]:
        """Heads from the simulation report object.

        Returns:
          Pandas Series containing the heads of the Nodes

        """
        return self._get(self.nodes, "Head", "m")

    @property
    def pressure(self) -> Union[pd.Series, pd.DataFrame]:
        """Pressures from the simulation report object.

        Returns:
          Pandas Series containing the pressures of the Nodes

        """
        return self._get(self.nodes, "Pressure", "m")

    @property
    def quality(self) -> Union[pd.Series, pd.DataFrame]:
        """Qualities from the simulation report object.

        Returns:
          Pandas Series containing the qualities of the Nodes

        """
        return self._get(self.nodes, "Quality")

    @property
    def length(self) -> Union[pd.Series, pd.DataFrame]:
        """Lengths from the simulation report object.

        Returns:
          Pandas Series containing the lengths of the Links

        """
        return self._get(self.links, "Length", "m")

    @property
    def diameter(self) -> Union[pd.Series, pd.DataFrame]:
        """Diameters from the simulation report object.

        Returns:
          Pandas Series containing the diameters of the Links

        """
        return self._get(self.links, "Diameter", "m")

    @property
    def flow(self) -> Union[pd.Series, pd.DataFrame]:
        """Flows from the simulation report object.

        Returns:
          Pandas Series containing the flows of the Links

        """
        return self._get(self.links, "Flow", "l/s")

    @property
    def velocity(self) -> Union[pd.Series, pd.DataFrame]:
        """Velocities from the simulation report object.

        Returns:
          Pandas Series containing the velocities of the Links

        """
        return self._get(self.links, "Velocity", "m/s")

    @property
    def headlossper1000m(self) -> Union[pd.Series, pd.DataFrame]:
        """Headlosses from the simulation report object as it is in the report (units in headloss per 1000m)

        Returns:
          Pandas Series containing the headlosses of the Links

        """
        return self._get(self.links, "Headloss", "/1000m")

    @property
    def headloss(self) -> Union[pd.Series, pd.DataFrame]:
        """Headlosses from the simulation report object.

        WARNING: If one wants to work with headloss, then the length reportparameter has to be set to 'YES' in the Network's Reportparameter settings.

        Returns:
          Pandas Series containing the headlosses of the Links

        """

        def convert(data):
            l = self.length
            l = l.replace(0, 1000.0)
            return l * data / 1000.0

        return self._get(self.links, "Headloss", "m", convert)

    @property
    def position(self) -> Union[pd.Series, pd.DataFrame]:
        """Positions from the simulation report object.

        Returns:
          Pandas Series containing the positions of the Links

        """
        return self._get(self.links, "Position")

    @property
    def settings(self):
        """Settings from the simulation report object.

        Returns:
          Pandas Series containing the settings of the Links

        """
        return self._get(self.links, "Setting")

    @property
    def reaction(self) -> Union[pd.Series, pd.DataFrame]:
        """Reactions from the simulation report object.

        Returns:
          Pandas Series containing the reactions of the Links

        """
        return self._get(self.links, "Reaction", "mass/L/day")

    @property
    def ffactor(self) -> Union[pd.Series, pd.DataFrame]:
        """Ffactors from the simulation report object.

        Returns:
          Pandas Series containing the ffactors of the Links

        """
        return self._get(self.links, "F-Factor")

    def get_node_info(self, id: str) -> pd.Series:
        """Gets the Node information from a simulation report object.

        Args:
          id: Node ID

        Returns:
          Pandas Series containing the information of the specified Node

        """
        return self._get_element_info(self.nodes, id)

    def get_link_info(self, id: str) -> pd.Series:
        """Gets the Link information from a simulation report object.

        Args:
          id: Link ID

        Returns:
          Pandas Series containing the information of the links

        """
        return self._get_element_info(self.links, id)
