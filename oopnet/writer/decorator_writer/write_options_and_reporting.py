import datetime
from io import TextIOWrapper
from typing import Union, Tuple

from oopnet.elements.base import QualityOption, DemandModel, BoolSetting, LimitSetting, ReportElementSetting
from oopnet.elements.network import Network
from oopnet.writer.decorator_writer.decorators import section_writer


def timedelta2hours(td: datetime.timedelta) -> str:
    """

    Args:
      td: 

    Returns:

    """
    dhours = td.days * 24
    hours, remainder = divmod(td.seconds, 3600)
    hours += dhours
    minutes, seconds = divmod(remainder, 60)
    return str(hours) + ':' + str(minutes).zfill(2)


def timedelta2startclocktime(t: datetime.timedelta) -> str:
    """

    Args:
      t: 

    Returns:

    """
    p = 'am'
    h = t.days * 24 + t.seconds / 3600
    if h > 12:
        p = 'pm'
        h -= 12
    m = t.seconds / 60 - t.seconds / 3600 * 60
    return str(int(h)).zfill(2) + ':' + str(int(m)).zfill(2) + ' ' + p


def reportparameter2str(rp: Union[BoolSetting, Tuple[LimitSetting, float]]) -> str:
    """

    Args:
      rp: 

    Returns:

    """
    if isinstance(rp, tuple):
        return f'{rp[0].value} {rp[1]}'
    else:
        return rp.value


def reportprecision2str(rp: int) -> str:
    """

    Args:
      rp: 

    Returns:

    """
    return f'PRECISION {rp}'


@section_writer('OPTIONS', 3)
def write_options(network: Network, fid: TextIOWrapper):
    """Writes network options to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[OPTIONS]', file=fid)
    if network.options:
        o = network.options
        if o.units:
            print('UNITS', o.units.value, file=fid)
        if o.headloss:
            print('HEADLOSS', o.headloss.value, file=fid)
        if o.hydraulics:
            print('HYDRAULICS', o.hydraulics[0].value, o.hydraulics[1], file=fid)
        if o.quality:
            if not isinstance(o.quality, list):
                print('QUALITY', o.quality, file=fid)
            elif o.quality[0] == QualityOption.AGE:
                print('QUALITY', o.quality[0].value, file=fid)
            elif o.quality[0] == QualityOption.CHEMICAL:
                print('QUALITY', o.quality[0].value, o.quality[1], o.quality[2], file=fid)
            elif o.quality[0] == QualityOption.TRACE:
                print('QUALITY', o.quality[0].value, o.quality[1].id, file=fid)
        else:
            print('QUALTIY', 'NONE', file=fid)
        if o.viscosity:
            print('VISCOSITY', o.viscosity, file=fid)
        if o.diffusivity:
            print('DIFFUSIVITY', o.diffusivity, file=fid)
        if o.specificgravity:
            print('SPECIFIC GRAVITY', o.specificgravity, file=fid)
        if o.trials:
            print('TRIALS', o.trials, file=fid)
        if o.accuracy:
            print('ACCURACY', str(o.accuracy).replace('e', 'E'), file=fid)
        if o.unbalanced:
            if not isinstance(o.unbalanced, tuple):
                print('UNBALANCED', o.unbalanced.value, file=fid)
            else:
                print('UNBALANCED', o.unbalanced[0].value, o.unbalanced[1], file=fid)
        if o.pattern:
            print('PATTERN', end=' ', file=fid)
            try:
                print(o.pattern.id, file=fid)
            except:
                print(o.pattern, file=fid)
        if o.demandmultiplier:
            print('DEMAND MULTIPLIER', o.demandmultiplier, file=fid)
        if o.emitterexponent:
            print('EMITTER EXPONENT', o.emitterexponent, file=fid)
        if o.tolerance:
            print('TOLERANCE', str(o.tolerance).replace('e', 'E'), file=fid)
        if o.map:
            print('MAP', o.map, file=fid)
        if o.demandmodel == DemandModel.PDA:
            print('DEMAND MODEL', o.demandmodel.value, file=fid)
            print('MINIMUM PRESSURE', o.minimumpressure, file=fid)
            print('REQUIRED PRESSURE', o.requiredpressure, file=fid)
            print('PRESSURE EXPONENT', o.pressureexponent, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('TIMES', 3)
def write_times(network: Network, fid: TextIOWrapper):
    """Writes time settings to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[TIMES]', file=fid)
    if network.times:
        t = network.times
        if t.duration:
            print('DURATION', timedelta2hours(t.duration), file=fid)
        if t.hydraulictimestep:
            print('HYDRAULIC TIMESTEP', timedelta2hours(t.hydraulictimestep), file=fid)
        if t.qualitytimestep:
            print('QUALITY TIMESTEP', timedelta2hours(t.qualitytimestep), file=fid)
        if t.ruletimestep:
            print('RULE TIMESTEP', timedelta2hours(t.ruletimestep), file=fid)
        if t.patterntimestep:
            print('PATTERN TIMESTEP', timedelta2hours(t.patterntimestep), file=fid)
        if t.patternstart:
            print('PATTERN START', timedelta2hours(t.patternstart), file=fid)
        if t.reporttimestep:
            print('REPORT TIMESTEP', timedelta2hours(t.reporttimestep), file=fid)
        if t.reportstart:
            print('REPORT START', timedelta2hours(t.reportstart), file=fid)
        if t.startclocktime:
            print('START CLOCKTIME', timedelta2startclocktime(t.startclocktime), file=fid)
        if t.statistic:
            print('STATISTIC', t.statistic.value, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('REPORT', 3)
def write_report(network: Network, fid: TextIOWrapper):
    """Writes report settings to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[REPORT]', file=fid)
    if network.report:
        r = network.report
        if r.pagesize:
            print('PAGESIZE', r.pagesize, file=fid)
        if r.file:
            print('FILE', r.file, file=fid)
        if r.status:
            print('STATUS', r.status.value, file=fid)
        if r.summary:
            print('SUMMARY', r.summary.value, file=fid)
        if r.energy:
            print('ENERGY', r.energy.value, file=fid)
        if r.nodes:
            if isinstance(r.nodes, ReportElementSetting):
                print('NODES', r.nodes.value, file=fid)
            else:
                print('NODES', end=' ', file=fid)
                for n in r.nodes:
                    print(n.id, end=' ', file=fid)
                print('\n', end=' ', file=fid)
        if r.links:
            if isinstance(r.links, ReportElementSetting):
                print('LINKS', r.links.value, file=fid)
            else:
                print('LINKS', end=' ', file=fid)
                for l in r.links:
                    print(l.id, end=' ', file=fid)
                print('\n', end=' ', file=fid)
    if network.reportparameter:
        r = network.reportparameter
        if r.elevation:
            print('ELEVATION', reportparameter2str(r.elevation), file=fid)
        if r.demand:
            print('DEMAND', reportparameter2str(r.demand), file=fid)
        if r.head:
            print('HEAD', reportparameter2str(r.head), file=fid)
        if r.pressure:
            print('PRESSURE', reportparameter2str(r.pressure), file=fid)
        if r.quality:
            print('QUALITY', reportparameter2str(r.quality), file=fid)
        if r.length:
            print('LENGTH', reportparameter2str(r.length), file=fid)
        if r.diameter:
            print('DIAMETER', reportparameter2str(r.diameter), file=fid)
        if r.flow:
            print('FLOW', reportparameter2str(r.flow), file=fid)
        if r.velocity:
            print('VELOCITY', reportparameter2str(r.velocity), file=fid)
        if r.headloss:
            print('HEADLOSS', reportparameter2str(r.headloss), file=fid)
        if r.setting:
            print('SETTING', reportparameter2str(r.setting), file=fid)
        if r.reaction:
            print('REACTION', reportparameter2str(r.reaction), file=fid)
        if r.ffactor:
            print('F-FACTOR', reportparameter2str(r.ffactor), file=fid)
    if network.reportprecision:
        r = network.reportprecision
        if r.elevation:
            print('ELEVATION', reportprecision2str(r.elevation), file=fid)
        if r.demand:
            print('DEMAND', reportprecision2str(r.demand), file=fid)
        if r.head:
            print('HEAD', reportprecision2str(r.head), file=fid)
        if r.pressure:
            print('PRESSURE', reportprecision2str(r.pressure), file=fid)
        if r.quality:
            print('QUALITY', reportprecision2str(r.quality), file=fid)
        if r.length:
            print('LENGTH', reportprecision2str(r.length), file=fid)
        if r.diameter:
            print('DIAMETER', reportprecision2str(r.diameter), file=fid)
        if r.flow:
            print('FLOW', reportprecision2str(r.flow), file=fid)
        if r.velocity:
            print('VELOCITY', reportprecision2str(r.velocity), file=fid)
        if r.headloss:
            print('HEADLOSS', reportprecision2str(r.headloss), file=fid)
        if r.position:
            print('POSITION', reportprecision2str(r.position), file=fid)
        if r.setting:
            print('SETTING', reportprecision2str(r.setting), file=fid)
        if r.reaction:
            print('REACTION', reportprecision2str(r.reaction), file=fid)
        if r.ffactor:
            print('F-FACTOR', reportparameter2str(r.ffactor), file=fid)
    print('\n', end=' ', file=fid)
