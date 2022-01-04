import datetime
from typing import Tuple, Union

from oopnet.elements.base import ReportParameterSetting, Unit, HeadlossFormula, HydraulicOption, QualityOption, \
    BalancingOption, DemandModel, StatisticSetting, BoolSetting, LimitSetting, ReportStatusSetting, \
    ReportElementSetting, ReportBoolSetting
from oopnet.elements.network import Network
from oopnet.utils.getters.get_by_id import get_node, get_link, get_pattern
from oopnet.reader.decorator_reader.decorators import section_reader


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
        if vals[1].upper() in ['SECONDS', 'SEC']:
            return datetime.timedelta(seconds=dt)
        elif vals[1].upper() in ['MINUTES', 'MIN']:
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


def parameter2report(vals: list) -> Union[BoolSetting, Tuple[LimitSetting, float]]:
    """

    Args:
      vals:

    Returns:

    """
    vals[1] = vals[1].upper()
    if vals[1] in ['YES', 'NO']:
        return BoolSetting[vals[1]]
    elif vals[1] in ['BELOW', 'ABOVE']:
        return LimitSetting[vals[1]], float(vals[2])


@section_reader('OPTIONS', 3)
def read_options(network: Network, block: list):
    """Reads options from block.

    Args:
      network: OOPNET network object where the options shall be stored
      block: EPANET input file block

    """
    for vals in block:
        vals = vals['values']
        o = network.options
        vals[0] = vals[0].upper()
        if vals[0] == 'UNITS':
            o.units = Unit[vals[1].upper()]
        elif vals[0] == 'HEADLOSS':
            o.headloss = HeadlossFormula.parse(vals[1].upper())
        elif vals[0] == 'HYDRAULICS':
            o.hydraulics = [HydraulicOption[vals[1].upper()], vals[2]]
        elif vals[0] == 'QUALITY':
            opt = QualityOption[vals[1].upper()]
            if len(vals) == 2:
                o.quality = opt
            if len(vals) > 3:
                if vals[1].upper() == 'CHEMICAL':
                    o.quality = (opt, vals[2], vals[3])
                elif vals[1].upper() == 'TRACE':
                    o.quality = (opt, get_node(network, vals[2]))
        elif vals[0] == 'VISCOSITY':
            o.viscosity = float(vals[1])
        elif vals[0] == 'DIFFUSIVITY':
            o.diffusivity = float(vals[1])
        elif vals[0] == 'SPECIFIC' and vals[1].upper() == 'GRAVITY':
            o.specificgravity = float(vals[2])
        elif vals[0] == 'TRIALS':
            o.trials = int(vals[1])
        elif vals[0] == 'ACCURACY':
            o.accuracy = float(vals[1])
        elif vals[0] == 'UNBALANCED':
            opt = BalancingOption[vals[1].upper()]
            if len(vals) == 2:
                o.unbalanced = opt
            if len(vals) > 2:
                o.unbalanced = (opt, int(vals[2]))
        elif vals[0] == 'PATTERN':
            try:
                o.pattern = get_pattern(network, vals[1])
            except:
                o.pattern = 1
        elif vals[0] == 'DEMAND' and vals[1].upper() == 'MULTIPLIER':
            o.demandmultiplier = float(vals[2])
        elif vals[0] == 'EMITTER' and vals[1].upper() == 'EXPONENT':
            o.emitterexponent = float(vals[2])
        elif vals[0] == 'TOLERANCE':
            o.tolerance = float(vals[1])
        elif vals[0] == 'MAP':
            o.map = vals[1]
        elif vals[0] == 'DEMAND' and vals[1].upper() == 'MODEL':
            o.demandmodel = DemandModel[vals[2]]
        elif vals[0] == 'MINIMUM' and vals[1].upper() == 'PRESSURE':
            o.minimumpressure = float(vals[2])
        elif vals[0] == 'REQUIRED' and vals[1].upper() == 'PRESSURE':
            o.requiredpressure = float(vals[2])
        elif vals[0] == 'PRESSURE' and vals[1].upper() == 'EXPONENT':
            o.pressureexponent = float(vals[2])
        if not o.demandmodel:
            o.demandmodel = DemandModel.DDA


@section_reader('TIMES', 3)
def read_times(network: Network, block: list):
    """Reads time settings from block.

    Args:
      network: OOPNET network object where the time settings shall be stored
      block: EPANET input file block

    """
    for vals in block:
        vals = vals['values']
        vals[0] = vals[0].upper()
        t = network.times
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
                if len(vals) > 3 and vals[3].upper() == 'PM':
                    h += 12
                t.startclocktime = datetime.timedelta(hours=h, minutes=m)
                            # timeformat = '%I:%M %p'
                            # t.startclocktime = datetime.datetime.strptime(vals[2] + ' ' + vals[3], timeformat)
            else:
                h = int(vals[2])
                if len(vals) > 3 and vals[3].upper() == 'PM':
                    h += 12
                t.startclocktime = datetime.timedelta(hours=h)
                            # timeformat = '%I %p'
                            # t.startclocktime = datetime.datetime.strptime(vals[2] + ' ' + vals[3], timeformat)
        elif vals[0] == 'STATISTIC':
            t.statistic = StatisticSetting(vals[1].upper())


@section_reader('REPORT', 3)
def read_report(network: Network, block: list):
    """Reads report settings from block.

    Args:
      network: OOPNET network object where the report settings shall be stored
      block: EPANET input file block

    """
    for vals in block:
        vals = vals['values']
        vals[0] = vals[0].upper()
        r = network.report
        param = network.reportparameter
        precision = network.reportprecision
        if vals[0] in ['PAGESIZE', 'PAGE']:
            r.pagesize = int(vals[1])
        elif vals[0] == 'FILE':
            r.file = vals[1]
        elif vals[0] == 'STATUS':
            r.status = ReportStatusSetting[vals[1].upper()]
        elif vals[0] == 'SUMMARY':
            r.summary = ReportBoolSetting[vals[1].upper()]
        elif vals[0] == 'ENERGY':
            r.energy = ReportBoolSetting[vals[1].upper()]
        elif vals[0] == 'NODES':
            if vals[1].upper() in ['NONE', 'ALL']:
                r.nodes = ReportElementSetting[vals[1].upper()]
            else:
                nodes = vals[1:]
                for n in nodes:
                    if r.nodes is None:
                        r.nodes = [get_node(network, n)]
                    else:
                        r.nodes.append(get_node(network, n))
        elif vals[0] == 'LINKS':
            if vals[1].upper() in ['NONE', 'ALL']:
                r.nodes = ReportElementSetting[vals[1].upper()]
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
