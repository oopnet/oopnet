from __future__ import annotations

from abc import abstractmethod

import datetime
from typing import Union, TYPE_CHECKING
import logging

from oopnet.utils.getters.element_lists import get_pattern_ids
from oopnet.utils.getters.get_by_id import get_node, get_link, get_pattern
from oopnet.reader.decorators import section_reader
from oopnet.elements.network_components import Node
from oopnet.elements.system_operation import Pattern
if TYPE_CHECKING:
    from oopnet.elements.network import Network


logger = logging.getLogger(__name__)


def time2timedelta(vals: list) -> datetime.timedelta:
    """

    Args:
      vals:

    Returns:

    """
    if ':' in vals[0]:
        dt = vals[0].split(':')
        if len(dt) == 2:
            return datetime.timedelta(hours=int(dt[0]), minutes=int(dt[1]))
        elif len(dt) == 3:
            return datetime.timedelta(hours=int(dt[0]), minutes=int(dt[1]), seconds=int(dt[2]))
    else:
        dt = float(vals[0])
        if len(vals) != 2:
            return datetime.timedelta(hours=dt)
        if vals[1].upper() in {'SECONDS', 'SEC'}:
            return datetime.timedelta(seconds=dt)
        elif vals[1].upper() in {'MINUTES', 'MIN'}:
            return datetime.timedelta(minutes=dt)
        elif vals[1].upper() == 'HOURS':
            return datetime.timedelta(hours=dt)
        elif vals[1].upper() == 'DAYS':
            return datetime.timedelta(days=dt)


def precision2report(vals: list) -> int:
    """

    Args:
      vals:

    Returns:

    """
    return int(vals[2])


def parameter2report(vals: list) -> Union[str, list[str, float]]:
    """

    Args:
      vals:

    Returns:

    """
    vals[1] = vals[1].upper()
    if vals[1] in ['YES', 'NO']:
        return vals[1]
    elif vals[1] in ['BELOW', 'ABOVE']:
        return [vals[1], float(vals[2])]


class OptionReportReader:
    _mapping = {}
    # _

    def __new__(cls, network, block):
        logger.debug('Reading Options')
        options = network.options
        for values in block:
            attr_name, attr_value = cls._parse_single(values, network)
            if attr_value is not None:
                setattr(options, attr_name, attr_value)

    @classmethod
    @abstractmethod
    def _parse_single(cls, values, network) -> tuple:
        pass


@section_reader('OPTIONS', 3)
class OptionReader(OptionReportReader):
    _mapping = {'UNITS': ('units', str),
                'HEADLOSS': ('headloss', str),
                'HYDRAULICS': ('hydraulics', str),
                'QUALITY': ('quality', str),
                'VISCOSITY': ('viscosity', float),
                'DIFFUSIVITY': ('diffusivity', float),
                'SPECIFIC': ('specificgravity', float),
                'TRIALS': ('trials', int),
                'ACCURACY': ('accuracy', float),
                'UNBALANCED': ('unbalanced', str),
                'PATTERN': ('pattern', Pattern),
                'DEMAND MULTIPLIER': ('demandmultiplier', float),
                'EMITTER': ('emitterexponent', float),
                'TOLERANCE': ('tolerance', float),
                'MAP': ('map', str),
                'DEMAND MODEL': ('demandmodel', str),
                'MINIMUM': ('minimumpressure', float),
                'REQUIRED': ('requiredpressure', float),
                'PRESSURE': ('pressureexponent', float)}

    @classmethod
    def _parse_single(cls, values: dict, network: Network) -> tuple:
        attr_values = values['values']
        name = attr_values[0].upper()
        if name == 'QUALITY':
            attr_value = cls._parse_quality(attr_values, network)
        elif name == 'HYDRAULICS':
            attr_value = cls._parse_hydraulics(attr_values)
        elif name == 'UNBALANCED':
            attr_value = cls._parse_unbalanced(attr_values)
        elif name == 'PATTERN':
            attr_value = cls._parse_pattern(attr_values, network)
        else:
            if name == 'DEMAND':
                if attr_values[1].upper() == 'MODEL':
                    name = 'DEMAND MODEL'
                elif attr_values[1].upper() == 'MULTIPLIER':
                    name = 'DEMAND MULTIPLIER'
            try:
                attr_cls = cls._mapping[name][1]
            except KeyError:
                return name, None
            attr_value = attr_cls(attr_values[-1])
        attr_name = cls._mapping[name][0]
        return attr_name, attr_value

    @classmethod
    def _parse_unbalanced(cls, values: list) -> Union[str, tuple[str, int]]:
        opt = values[1].upper()
        if len(values) == 2:
            return opt
        if len(values) == 3:
            return opt, int(values[2])

    @classmethod
    def _parse_hydraulics(cls, values: list) -> list[str]:
        return [values[1].upper(), values[2]]

    @classmethod
    def _parse_quality(cls, values: list, network: Network) -> Union[str, tuple[str, str, str],
                                                                     tuple[str, Node]]:
        opt = values[1].upper()
        if len(values) == 2:
            return opt
        if len(values) > 3:
            if values[1].upper() == 'CHEMICAL':
                return opt, values[2], values[3]
            elif values[1].upper() == 'TRACE':
                return opt, get_node(network, values[2])

    @classmethod
    def _parse_pattern(cls, values: list, network: Network) -> Union[Pattern, int]:
        if values[1] in get_pattern_ids(network):
            return get_pattern(network, values[1])
        else:
            return 1


# @section_reader('TIMES', 3)
class TimesReader(OptionReportReader):
    _mapping = {'DURATION': ('duration', 'time2timedelta'),
                'HYDRAULIC': ('hydraulic', 'time2timedelta'),
                'QUALITY': ('quality', 'time2timedelta'),
                }


@section_reader('TIMES', 3)
def read_times(network: Network, block: list):
    """Reads time settings from block.

    Args:
      network: OOPNET network object where the time settings shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading times settings')
    t = network.times
    for vals in block:
        vals = vals['values']
        vals[0] = vals[0].upper()
        if vals[0] == 'DURATION':
            t.duration = time2timedelta(vals[1:])
        elif vals[0] == 'HYDRAULIC' and vals[1].upper() == 'TIMESTEP':
            t.hydraulictimestep = time2timedelta(vals[2:])
        elif vals[0] == 'QUALITY' and vals[1].upper() == 'TIMESTEP':
            t.qualitytimestep = time2timedelta(vals[2:])
        elif vals[0] == 'RULE' and vals[1].upper() == 'TIMESTEP':
            t.ruletimestep = time2timedelta(vals[2:])
        elif vals[0] == 'PATTERN' and vals[1].upper() == 'TIMESTEP':
            t.patterntimestep = time2timedelta(vals[2:])
        elif vals[0] == 'PATTERN' and vals[1].upper() == 'START':
            t.patternstart = time2timedelta(vals[2:])
        elif vals[0] == 'REPORT' and vals[1].upper() == 'TIMESTEP':
            t.reporttimestep = time2timedelta(vals[2:])
        elif vals[0] == 'REPORT' and vals[1].upper() == 'START':
            t.reportstart = time2timedelta(vals[2:])
        elif vals[0] == 'START' and vals[1].upper() == 'CLOCKTIME':
            if ':' in vals[2]:
                h, m = list(map(int, vals[2].split(':')))  # todo: catch seconds, then three values are there to unpack
                h = h if h != 12 or len(vals) == 4 and vals[3].upper() != 'AM' else 0
                if len(vals) > 3 and vals[3].upper() == 'PM':
                    h += 12
                t.startclocktime = datetime.timedelta(hours=h, minutes=m)
                # timeformat = '%I:%M %p'
                # t.startclocktime = datetime.datetime.strptime(vals[2] + ' ' + vals[3], timeformat)
            else:
                h = int(vals[2]) if vals[2] != '12' or vals[3].upper() != 'AM' else 0
                if len(vals) > 3 and vals[3].upper() == 'PM':
                    h += 12
                t.startclocktime = datetime.timedelta(hours=h)
                # timeformat = '%I %p'
                # t.startclocktime = datetime.datetime.strptime(vals[2] + ' ' + vals[3], timeformat)
        elif vals[0] == 'STATISTIC':
            t.statistic = vals[1].upper()


@section_reader('REPORT', 3)
def read_report(network: Network, block: list):
    """Reads report settings from block.

    Args:
      network: OOPNET network object where the report settings shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading report settings')
    r = network.report
    param = network.reportparameter
    precision = network.reportprecision
    for vals in block:
        vals = vals['values']
        vals[0] = vals[0].upper()
        if vals[0] in ['PAGESIZE', 'PAGE']:
            r.pagesize = int(vals[1])
        elif vals[0] == 'FILE':
            r.file = vals[1]
        elif vals[0] == 'STATUS':
            r.status = vals[1].upper()
        elif vals[0] == 'SUMMARY':
            r.summary = vals[1].upper()
        elif vals[0] == 'ENERGY':
            r.energy = vals[1].upper()
        elif vals[0] == 'NODES':
            if vals[1].upper() in ['NONE', 'ALL']:
                r.nodes = vals[1].upper()
            else:
                nodes = vals[1:]
                for n in nodes:
                    if r.nodes is None:
                        r.nodes = [get_node(network, n)]
                    else:
                        r.nodes.append(get_node(network, n))
        elif vals[0] == 'LINKS':
            if vals[1].upper() in ['NONE', 'ALL']:
                r.nodes = vals[1].upper()
            else:
                links = vals[1:]
                for l in links:
                    if r.links is None:
                        r.links = [get_link(network, l)]
                    else:
                        r.links.append(get_link(network, l))
        elif vals[1].upper() == 'PRECISION':
            if vals[0] == 'ELEVATION':
                precision.elevation = precision2report(vals)
            elif vals[0] == 'DEMAND':
                precision.demand = precision2report(vals)
            elif vals[0] == 'HEAD':
                precision.head = precision2report(vals)
            elif vals[0] == 'PRESSURE':
                precision.pressure = precision2report(vals)
            elif vals[0] == 'QUALITY':
                precision.quality = precision2report(vals)
            elif vals[0] == 'LENGTH':
                precision.length = precision2report(vals)
            elif vals[0] == 'DIAMETER':
                precision.diameter = precision2report(vals)
            elif vals[0] == 'FLOW':
                precision.flow = precision2report(vals)
            elif vals[0] == 'VELOCITY':
                precision.velocity = precision2report(vals)
            elif vals[0] == 'HEADLOSS':
                precision.headloss = precision2report(vals)
            elif vals[0] == 'POSITION':
                precision.position = precision2report(vals)
            elif vals[0] == 'SETTING':
                precision.setting = precision2report(vals)
            elif vals[0] == 'REACTION':
                precision.reaction = precision2report(vals)
            elif vals[0] == 'F-FACTOR':
                precision.ffactor = precision2report(vals)
        elif vals[0] == 'ELEVATION':
            param.elevation = parameter2report(vals)
        elif vals[0] == 'DEMAND':
            param.demand = parameter2report(vals)
        elif vals[0] == 'HEAD':
            param.head = parameter2report(vals)
        elif vals[0] == 'PRESSURE':
            param.pressure = parameter2report(vals)
        elif vals[0] == 'QUALITY':
            param.quality = parameter2report(vals)
        elif vals[0] == 'LENGTH':
            param.length = parameter2report(vals)
        elif vals[0] == 'DIAMETER':
            param.diameter = parameter2report(vals)
        elif vals[0] == 'FLOW':
            param.flow = parameter2report(vals)
        elif vals[0] == 'VELOCITY':
            param.velocity = parameter2report(vals)
        elif vals[0] == 'HEADLOSS':
            param.headloss = parameter2report(vals)
        elif vals[0] == 'POSITION':
            param.position = parameter2report(vals)
        elif vals[0] == 'SETTING':
            param.setting = parameter2report(vals)
        elif vals[0] == 'REACTION':
            param.reaction = parameter2report(vals)
        elif vals[0] == 'F-FACTOR':
            param.ffactor = parameter2report(vals)
