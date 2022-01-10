import datetime
from typing import Optional, Union, Type

from xarray import DataArray, Dataset

from oopnet.report.binaryfile_reader import BinaryFileReader
from oopnet.report.reportfile_reader import ReportFileReader


class Report:
    """ """
    def __new__(cls, filename: str, startdatetime: Optional[datetime.datetime] = None, reader: Union[Type[BinaryFileReader], Type[ReportFileReader]] = ReportFileReader) -> tuple[Union[DataArray, Dataset, None], Union[DataArray, Dataset, None]]:
        return reader(filename, startdatetime)
