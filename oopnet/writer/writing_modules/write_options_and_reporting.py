from __future__ import annotations
from typing import TYPE_CHECKING
import datetime
from io import TextIOWrapper
from typing import Union
import logging

from oopnet.writer.decorators import section_writer
if TYPE_CHECKING:
    from oopnet.elements.network import Network

logger = logging.getLogger(__name__)


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


def reportparameter2str(rp: Union[str, list[str, float]]) -> str:
    """

    Args:
      rp: 

    Returns:

    """
    return f'{rp[0]} {rp[1]}' if isinstance(rp, list) else rp


def reportprecision2str(rp: int) -> str:
    """

    Args:
      rp: 

    Returns:

    """
    if rp > 3:
        logger.debug(f'Limiting report parameter precision from {rp} to 3')
        rp = 3
    return f'PRECISION {rp}'


@section_writer('OPTIONS', 3)
def write_options(network: Network, fid: TextIOWrapper):
    """Writes network options to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Options section')
    print('[OPTIONS]', file=fid)
    o = network.options
    print('UNITS', o.units, file=fid)
    print('HEADLOSS', o.headloss, file=fid)
    if o.hydraulics:
        print('HYDRAULICS', o.hydraulics[0], o.hydraulics[1], file=fid)
    if not isinstance(o.quality, list):
        print('QUALITY', o.quality, file=fid)
    elif o.quality[0] == 'AGE':
        print('QUALITY', o.quality[0], file=fid)
    elif o.quality[0] == 'CHEMICAL':
        print('QUALITY', o.quality[0], o.quality[1], o.quality[2], file=fid)
    elif o.quality[0] == 'TRACE':
        print('QUALITY', o.quality[0], o.quality[1].id, file=fid)
    else:
        print('QUALTIY', 'NONE', file=fid)
    print('VISCOSITY', o.viscosity, file=fid)
    print('DIFFUSIVITY', o.diffusivity, file=fid)
    print('SPECIFIC GRAVITY', o.specificgravity, file=fid)
    print('TRIALS', o.trials, file=fid)
    print('ACCURACY', str(o.accuracy).replace('e', 'E'), file=fid)
    if not isinstance(o.unbalanced, tuple):
        print('UNBALANCED', o.unbalanced, file=fid)
    else:
        print('UNBALANCED', o.unbalanced[0], o.unbalanced[1], file=fid)
    print('PATTERN', end=' ', file=fid)
    try:
        print(o.pattern.id, file=fid)
    except:
        print(o.pattern, file=fid)
    print('DEMAND MULTIPLIER', o.demandmultiplier, file=fid)
    print('EMITTER EXPONENT', o.emitterexponent, file=fid)
    print('TOLERANCE', str(o.tolerance).replace('e', 'E'), file=fid)
    if o.map:
        print('MAP', o.map, file=fid)
    if o.demandmodel == 'PDA':
        print('DEMAND MODEL', o.demandmodel, file=fid)
        print('MINIMUM PRESSURE', o.minimumpressure, file=fid)
        print('REQUIRED PRESSURE', o.requiredpressure, file=fid)
        print('PRESSURE EXPONENT', o.pressureexponent, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('TIMES', 3)
def write_times(network: Network, fid: TextIOWrapper):
    """Writes time settings to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Times section')
    print('[TIMES]', file=fid)
    t = network.times
    print('DURATION', timedelta2hours(t.duration), file=fid)
    print('HYDRAULIC TIMESTEP', timedelta2hours(t.hydraulictimestep), file=fid)
    if t.qualitytimestep:
        print('QUALITY TIMESTEP', timedelta2hours(t.qualitytimestep), file=fid)
    if t.ruletimestep:
        print('RULE TIMESTEP', timedelta2hours(t.ruletimestep), file=fid)
    if t.patterntimestep:
        print('PATTERN TIMESTEP', timedelta2hours(t.patterntimestep), file=fid)
    print('PATTERN START', timedelta2hours(t.patternstart), file=fid)
    print('REPORT TIMESTEP', timedelta2hours(t.reporttimestep), file=fid)
    print('REPORT START', timedelta2hours(t.reportstart), file=fid)
    print('START CLOCKTIME', timedelta2startclocktime(t.startclocktime), file=fid)
    print('STATISTIC', t.statistic, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('REPORT', 3)
def write_report(network: Network, fid: TextIOWrapper):
    """Writes report settings to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Report section')
    print('[REPORT]', file=fid)
    r = network.report
    print('PAGESIZE', r.pagesize, file=fid)
    if r.file:
        print('FILE', r.file, file=fid)
    print('STATUS', r.status, file=fid)
    print('SUMMARY', r.summary, file=fid)
    print('ENERGY', r.energy, file=fid)
    if isinstance(r.nodes, str):
        print('NODES', r.nodes, file=fid)
    else:
        print('NODES', end=' ', file=fid)
        for n in r.nodes:
            print(n.id, end=' ', file=fid)
        print('\n', end=' ', file=fid)
    if isinstance(r.links, str):
        print('LINKS', r.links, file=fid)
    else:
        print('LINKS', end=' ', file=fid)
        for l in r.links:
            print(l.id, end=' ', file=fid)
        print('\n', end=' ', file=fid)
    r = network.reportparameter
    print('ELEVATION', reportparameter2str(r.elevation), file=fid)
    print('DEMAND', reportparameter2str(r.demand), file=fid)
    print('HEAD', reportparameter2str(r.head), file=fid)
    print('PRESSURE', reportparameter2str(r.pressure), file=fid)
    print('QUALITY', reportparameter2str(r.quality), file=fid)
    print('LENGTH', reportparameter2str(r.length), file=fid)
    print('DIAMETER', reportparameter2str(r.diameter), file=fid)
    print('FLOW', reportparameter2str(r.flow), file=fid)
    print('VELOCITY', reportparameter2str(r.velocity), file=fid)
    print('HEADLOSS', reportparameter2str(r.headloss), file=fid)
    print('SETTING', reportparameter2str(r.setting), file=fid)
    print('REACTION', reportparameter2str(r.reaction), file=fid)
    print('F-FACTOR', reportparameter2str(r.ffactor), file=fid)
    r = network.reportprecision
    print('ELEVATION', reportprecision2str(r.elevation), file=fid)
    print('DEMAND', reportprecision2str(r.demand), file=fid)
    print('HEAD', reportprecision2str(r.head), file=fid)
    print('PRESSURE', reportprecision2str(r.pressure), file=fid)
    print('QUALITY', reportprecision2str(r.quality), file=fid)
    print('LENGTH', reportprecision2str(r.length), file=fid)
    print('DIAMETER', reportprecision2str(r.diameter), file=fid)
    print('FLOW', reportprecision2str(r.flow), file=fid)
    print('VELOCITY', reportprecision2str(r.velocity), file=fid)
    print('HEADLOSS', reportprecision2str(r.headloss), file=fid)
    print('SETTING', reportprecision2str(r.setting), file=fid)
    print('REACTION', reportprecision2str(r.reaction), file=fid)
    print('F-FACTOR', reportprecision2str(r.ffactor), file=fid)
    print('\n', end=' ', file=fid)
