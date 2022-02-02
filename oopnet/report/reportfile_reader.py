from typing import Optional, Union
import datetime
import re
import logging

import pandas as pd
import xarray as xr
from xarray import DataArray, Dataset

from oopnet.report.error_manager import ErrorManager
from oopnet.utils.oopnet_logging import logging_decorator

logger = logging.getLogger(__name__)


def str2hms(timestring: str) -> tuple[int, int, float]:
    """Converts a string to a tuple containing hours, minutes and seconds.

    Args:
      timestring: string to be parsed

    Returns:
        parsed timestring as a tuple
    """
    vals = timestring.split(':')
    hours = int(vals[0])
    minutes = int(vals[1])
    seconds = float(vals[2]) if len(vals) > 2 else 0
    return hours, minutes, seconds


def blockkey2typetime(blockkey: str, startdatetime: Optional[datetime.datetime] = None) -> tuple[str, datetime.datetime]:
    """

    Args:
      blockkey:
      startdatetime: (Default value = None)

    Returns:

    """

    vals = blockkey.split()
    kind = vals[0]

    if len(vals) > 3:
        time = vals[3]
        hours, minutes, seconds = str2hms(time)
        if startdatetime is None:
            today = datetime.datetime(year=2016, month=1, day=1, hour=0, minute=0, second=0)
        else:
            today = startdatetime
        time = today + datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        # time = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    else:
        time = None
    return kind, time


def lst2xray(lst: list) -> xr.DataArray:
    """

    Args:
      lst: list:

    Returns:

    """
    lst[2:] = [x[:len(lst[0])+1] for x in lst[2:]]
    frame = pd.DataFrame.from_dict(lst[2:])
    frame.columns = ['id'] + lst[0]
    frame[lst[0]] = frame[lst[0]].applymap(float)
    frame.set_index('id', inplace=True)

    return xr.DataArray(frame)


# todo: refactor
@logging_decorator(logger)
class ReportFileReader:
    def __new__(cls, filename: str, startdatetime: Optional[datetime.datetime] = None) -> tuple[Union[DataArray, Dataset, None], Union[DataArray, Dataset, None]]:
        logger.debug('Reading Report File')
        with open(filename, 'r') as fid:
            content = fid.readlines()
            # print(content)
            block = {}
            key = 'start'
            block[key] = []
            error_manager = ErrorManager()
            error_found = False

            for linenumber, line in enumerate(content):
                if error_found and len(line.strip()) != 0:
                    error_manager.append_error_details(line)

                error_found = error_manager.check_line(line)
                if len(line.strip()) == 0:
                    key = content[linenumber+1]
                    key = re.sub(r'\s+', ' ', key.replace('\n', '').strip())
                    block[key] = []
                else:
                    line = re.sub(r'\s+', ' ', line.replace('\n', '').strip())
                    if line not in key and (
                        line in key or not line.startswith('---------')
                    ):
                        block[key].append(line.split(' '))
        error_manager.raise_errors()
        links = None
        nodes = None
        data = None

        format = '%y.%m.%d %H:%M:%S'
        for k in list(block.keys()):
            if 'Node' not in k and 'Link' not in k:
                block.pop(k)

        for kind in ['Node', 'Link']:
            times = []
            # for key in sorted(block.iterkeys(), key=lambda x: x.split(' ')[3].zfill(8)):
            for key in sorted(block.keys()):
                if key.startswith(kind):
                    kind, time = blockkey2typetime(key, startdatetime=startdatetime)
                    if time is not None:
                        times.append(time)

            frames = []
            for key in sorted(block.keys()):
                if key.startswith(kind):
                    lst = block[key]
                    x = lst2xray(lst)
                    frames.append(x)
            if frames:
                if times:
                    data = xr.concat(frames, times)
                    data = data.rename({'concat_dim': 'time', 'dim_1': 'vars'})
                else:
                    data = frames[0]
                    data = data.rename({'dim_1': 'vars'})
            if kind == 'Node':
                nodes = data
            else:
                links = data

        return nodes, links