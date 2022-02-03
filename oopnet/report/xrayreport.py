import datetime
from typing import Optional, Union, Type, Callable
import logging

import pandas as pd
from xarray import DataArray, Dataset

from oopnet.report.binaryfile_reader import BinaryFileReader
from oopnet.report.reportfile_reader import ReportFileReader

logger = logging.getLogger(__name__)


# todo: add documentation
class Report:
    """Class for storing stimulation results.


    """
    nodes: DataArray
    links: DataArray

    def __init__(self, filename: str, startdatetime: Optional[datetime.datetime] = None,
                 reader: Union[Type[BinaryFileReader], Type[ReportFileReader]] = ReportFileReader):
        logger.debug('Creating report.')
        self.nodes, self.links = reader(filename, startdatetime)

    @staticmethod
    def _get(array: DataArray, var: str, unit: Optional[str] = None, calc: Optional[Callable] = None):
        data = array.sel(vars=var).to_pandas()
        if calc:
            data = calc(data)

        if unit:
            data.name = f'{var} ({unit})'
        else:
            data.name = var
        return data

    @property
    def elevation(self) -> pd.Series:
        """Function for getting the elevations from the simulation report object.

        Returns:
          Pandas Series containing the elevations of the nodes

        """
        return self._get(self.nodes, 'Elevation',  'm')

    @property
    def demand(self) -> pd.Series:
        """Function for getting the demands from the simulation report object.

        Returns:
          Pandas Series containing the demands of the nodes

        """
        return self._get(self.nodes, 'Demand', 'l/s')

    @property
    def head(self) -> pd.Series:
        """Function for getting the heads from the simulation report object.

        Returns:
          Pandas Series containing the heads of the nodes

        """
        return self._get(self.nodes, 'Head', 'm')

    @property
    def pressure(self) -> pd.Series:
        """Function for getting the pressures from the simulation report object.

        Returns:
          Pandas Series containing the pressures of the nodes

        """
        return self._get(self.nodes, 'Pressure', 'm')

    @property
    def quality(self) -> pd.Series:
        """Function for getting the qualities from the simulation report object.

        Returns:
          Pandas Series containing the qualities of the nodes

        """
        return self._get(self.nodes, 'Quality')

    @property
    def length(self) -> pd.Series:
        """Function for getting the lengths from the simulation report object.

        Returns:
          Pandas Series containing the lengths of the links

        """
        return self._get(self.links, 'Length', 'm')

    @property
    def diameter(self) -> pd.Series:
        """Function for getting the diameters from the simulation report object.

        Returns:
          Pandas Series containing the diameters of the links

        """
        return self._get(self.links, 'Diameter', 'm')

    @property
    def flow(self) -> pd.Series:
        """Function for getting the flows from the simulation report object.

        Returns:
          Pandas Series containing the flows of the links

        """
        return self._get(self.links, 'Flow', 'l/s')

    @property
    def velocity(self) -> pd.Series:
        """Function for getting the velocities from the simulation report object.

        Returns:
          Pandas Series containing the velocities of the links

        """
        return self._get(self.links, 'Velocity', 'm/s')

    @property
    def headlossper1000m(self) -> pd.Series:
        """Function for getting the headlosses from the simulation report object as it is in the report (units in headloss
        per 1000m)

        Returns:
          Pandas Series containing the headlosses of the links

        """
        return self._get(self.links, 'Headloss', '/1000m')

    @property
    def headloss(self) -> pd.Series:
        """Function for getting the headlosses from the simulation report object.

        WARNING: If one wants to work with headloss, then the length has to be defined in the report

        Returns:
          Pandas Series containing the headlosses of the links

        """
        def calc(data):
            return self.length * data / 1000.0
        return self._get(self.links, 'Headloss', 'm', calc)

    @property
    def position(self) -> pd.Series:
        """Function for getting the positions from the simulation report object.

        Returns:
          Pandas Series containing the positions of the links

        """
        return self._get(self.links, 'Position')

    @property
    def settings(self):
        """Function for getting the settings from the simulation report object.

        Returns:
          Pandas Series containing the settings of the links

        """
        return self._get(self.links, 'Setting')

    @property
    def reaction(self) -> pd.Series:
        """Function for getting the reactions from the simulation report object.

        Returns:
          Pandas Series containing the reactions of the links

        """
        return self._get(self.links, 'Reaction', 'mass/L/day')

    @property
    def friction_factor(self) -> pd.Series:
        """Function for getting the ffactors from the simulation report object.

        Returns:
          Pandas Series containing the ffactors of the links

        """
        return self._get(self.links, 'F-Factor')
