import datetime
from typing import Optional, Union, Type, Callable
import logging

import pandas as pd
from xarray import DataArray, Dataset

from oopnet.report.binaryfile_reader import BinaryFileReader
from oopnet.report.reportfile_reader import ReportFileReader

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

    def __init__(self, filename: str, startdatetime: Optional[datetime.datetime] = None,
                 reader: Union[Type[BinaryFileReader], Type[ReportFileReader]] = ReportFileReader):
        """SimulationReport init method.

        Args:
            filename: name of EPANET input file be simulated
            startdatetime:
            reader: specifies whether the report or the binary file created by EPANET are read

        """
        logger.debug('Creating report.')
        self.nodes, self.links = reader(filename, startdatetime)

    @staticmethod
    def _get(array: DataArray, var: str, unit: Optional[str] = None, calc: Optional[Callable] = None):
        data = array.sel(vars=var).to_pandas()
        if calc:
            data = calc(data)
        data.name = f'{var} ({unit})' if unit else var
        return data

    @staticmethod
    def _get_element_info(array: DataArray, id: str) -> pd.Series:
        data = array.sel(id=id).to_pandas()
        data.name = id
        return data

    @property
    def elevation(self) -> pd.Series:
        """Elevations from the simulation report object.

        Returns:
          Pandas Series containing the elevations of the Nodes

        """
        return self._get(self.nodes, 'Elevation',  'm')

    @property
    def demand(self) -> pd.Series:
        """Demands from the simulation report object.

        Returns:
          Pandas Series containing the demands of the Nodes

        """
        return self._get(self.nodes, 'Demand', 'l/s')

    @property
    def head(self) -> pd.Series:
        """Heads from the simulation report object.

        Returns:
          Pandas Series containing the heads of the Nodes

        """
        return self._get(self.nodes, 'Head', 'm')

    @property
    def pressure(self) -> pd.Series:
        """Pressures from the simulation report object.

        Returns:
          Pandas Series containing the pressures of the Nodes

        """
        return self._get(self.nodes, 'Pressure', 'm')

    @property
    def quality(self) -> pd.Series:
        """Qualities from the simulation report object.

        Returns:
          Pandas Series containing the qualities of the Nodes

        """
        return self._get(self.nodes, 'Quality')

    @property
    def length(self) -> pd.Series:
        """Lengths from the simulation report object.

        Returns:
          Pandas Series containing the lengths of the Links

        """
        return self._get(self.links, 'Length', 'm')

    @property
    def diameter(self) -> pd.Series:
        """Diameters from the simulation report object.

        Returns:
          Pandas Series containing the diameters of the Links

        """
        return self._get(self.links, 'Diameter', 'm')

    @property
    def flow(self) -> pd.Series:
        """Flows from the simulation report object.

        Returns:
          Pandas Series containing the flows of the Links

        """
        return self._get(self.links, 'Flow', 'l/s')

    @property
    def velocity(self) -> pd.Series:
        """Velocities from the simulation report object.

        Returns:
          Pandas Series containing the velocities of the Links

        """
        return self._get(self.links, 'Velocity', 'm/s')

    @property
    def headlossper1000m(self) -> pd.Series:
        """Headlosses from the simulation report object as it is in the report (units in headloss per 1000m)

        Returns:
          Pandas Series containing the headlosses of the Links

        """
        return self._get(self.links, 'Headloss', '/1000m')

    @property
    def headloss(self) -> pd.Series:
        """Headlosses from the simulation report object.

        WARNING: If one wants to work with headloss, then the length reportparameter has to be set to 'YES' in the Network's Reportparameter settings.

        Returns:
          Pandas Series containing the headlosses of the Links

        """
        def convert(data):
            return self.length * data / 1000.0
        return self._get(self.links, 'Headloss', 'm', convert)

    @property
    def position(self) -> pd.Series:
        """Positions from the simulation report object.

        Returns:
          Pandas Series containing the positions of the Links

        """
        return self._get(self.links, 'Position')

    @property
    def settings(self):
        """Settings from the simulation report object.

        Returns:
          Pandas Series containing the settings of the Links

        """
        return self._get(self.links, 'Setting')

    @property
    def reaction(self) -> pd.Series:
        """Reactions from the simulation report object.

        Returns:
          Pandas Series containing the reactions of the Links

        """
        return self._get(self.links, 'Reaction', 'mass/L/day')

    @property
    def ffactor(self) -> pd.Series:
        """Ffactors from the simulation report object.

        Returns:
          Pandas Series containing the ffactors of the Links

        """
        return self._get(self.links, 'F-Factor')

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
