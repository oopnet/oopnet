from io import TextIOWrapper

from oopnet.elements.network import Network

from .decorators import section_writer


def timedelta2hours(td):
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


def timedelta2startclocktime(t):
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


def reportparameter2str(rp):
    """

    Args:
      rp: 

    Returns:

    """
    if rp == 'YES':
        return 'YES'
    elif rp == 'NO':
        return 'NO'
    if isinstance(rp, list):
        return rp[0] + ' ' + str(rp[1])


def reportprecision2str(rp):
    """

    Args:
      rp: 

    Returns:

    """
    return 'PRECISION ' + str(rp)


@section_writer('OPTIONS', 3)
def write_options(network: Network, fid: TextIOWrapper):
    """Writes network options to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[OPTIONS]', file=fid)
    if network.options is not None:
        o = network.options
        if o.units is not None:
            print('UNITS', o.units, file=fid)
        if o.headloss is not None:
            print('HEADLOSS', o.headloss, file=fid)
        if o.hydraulics is not None:
            print('HYDRAULICS', o.hydraulics[0], o.hydraulics[1], file=fid)
        if o.quality is not None:
            if not isinstance(o.quality, list):
                print('QUALITY', o.quality, file=fid)
            else:
                if o.quality[0] == 'AGE':
                    print('QUALITY', o.quality[0], file=fid)
                elif o.quality[0] == 'CHEMICAL':
                    print('QUALITY', o.quality[0], o.quality[1], o.quality[2], file=fid)
                elif o.quality[0] == 'TRACE':
                    print('QUALITY', o.quality[0], o.quality[1].id, file=fid)
        else:
            print('QUALTIY', 'NONE', file=fid)
        if o.viscosity is not None:
            print('VISCOSITY', o.viscosity, file=fid)
        if o.diffusivity is not None:
            print('DIFFUSIVITY', o.diffusivity, file=fid)
        if o.specificgravity is not None:
            print('SPECIFIC GRAVITY', o.specificgravity, file=fid)
        if o.trials is not None:
            print('TRIALS', o.trials, file=fid)
        if o.accuracy is not None:
            print('ACCURACY', str(o.accuracy).replace('e', 'E'), file=fid)
        if o.unbalanced is not None:
            if not isinstance(o.unbalanced, list):
                print('UNBALANCED', o.unbalanced, file=fid)
            else:
                print('UNBALANCED', o.unbalanced[0], o.unbalanced[1], file=fid)
        if o.pattern is not None:
            print('PATTERN', end=' ', file=fid)
            try:
                print(o.pattern.id, file=fid)
            except:
                print(o.pattern, file=fid)
        if o.demandmultiplier is not None:
            print('DEMAND MULTIPLIER', o.demandmultiplier, file=fid)
        if o.emitterexponent is not None:
            print('EMITTER EXPONENT', o.emitterexponent, file=fid)
        if o.tolerance is not None:
            print('TOLERANCE', str(o.tolerance).replace('e', 'E'), file=fid)
        if o.map is not None:
            print('MAP', o.map, file=fid)
        if o.demandmodel == 'PDA':
            print('DEMAND MODEL', 'PDA', file=fid)
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
    if network.times is not None:
        t = network.times
        if t.duration is not None:
            print('DURATION', timedelta2hours(t.duration), file=fid)
        if t.hydraulictimestep is not None:
            print('HYDRAULIC TIMESTEP', timedelta2hours(t.hydraulictimestep), file=fid)
        if t.qualitytimestep is not None:
            print('QUALITY TIMESTEP', timedelta2hours(t.qualitytimestep), file=fid)
        if t.ruletimestep is not None:
            print('RULE TIMESTEP', timedelta2hours(t.ruletimestep), file=fid)
        if t.patterntimestep is not None:
            print('PATTERN TIMESTEP', timedelta2hours(t.patterntimestep), file=fid)
        if t.patternstart is not None:
            print('PATTERN START', timedelta2hours(t.patternstart), file=fid)
        if t.reporttimestep is not None:
            print('REPORT TIMESTEP', timedelta2hours(t.reporttimestep), file=fid)
        if t.reportstart is not None:
            print('REPORT START', timedelta2hours(t.reportstart), file=fid)
        if t.startclocktime is not None:
            print('START CLOCKTIME', timedelta2startclocktime(t.startclocktime), file=fid)
        if t.statistic is not None:
            print('STATISTIC', t.statistic, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('REPORT', 3)
def write_report(network: Network, fid: TextIOWrapper):
    """Writes report settings to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[REPORT]', file=fid)
    if network.report is not None:
        r = network.report
        if r.pagesize is not None:
            print('PAGESIZE', r.pagesize, file=fid)
        if r.file is not None:
            print('FILE', r.file, file=fid)
        if r.status is not None:
            print('STATUS', r.status, file=fid)
        if r.summary is not None:
            print('SUMMARY', r.summary, file=fid)
        if r.energy is not None:
            print('ENERGY', r.energy, file=fid)
        if r.nodes is not None:
            if r.nodes == 'NONE' or r.nodes == 'ALL':
                print('NODES', r.nodes, file=fid)
            else:
                print('NODES', end=' ', file=fid)
                for n in r.nodes:
                    print(n.id, end=' ', file=fid)
                print('\n', end=' ', file=fid)
        if r.links is not None:
            if r.links == 'NONE' or r.links == 'ALL':
                print('LINKS', r.links, file=fid)
            else:
                print('LINKS', end=' ', file=fid)
                for l in r.links:
                    print(l.id, end=' ', file=fid)
                print('\n', end=' ', file=fid)
    if network.reportparameter is not None:
        r = network.reportparameter
        if r.elevation is not None:
            print('ELEVATION', reportparameter2str(r.elevation), file=fid)
        if r.demand is not None:
            print('DEMAND', reportparameter2str(r.demand), file=fid)
        if r.head is not None:
            print('HEAD', reportparameter2str(r.head), file=fid)
        if r.pressure is not None:
            print('PRESSURE', reportparameter2str(r.pressure), file=fid)
        if r.quality is not None:
            print('QUALITY', reportparameter2str(r.quality), file=fid)
        if r.length is not None:
            print('LENGTH', reportparameter2str(r.length), file=fid)
        if r.diameter is not None:
            print('DIAMETER', reportparameter2str(r.diameter), file=fid)
        if r.flow is not None:
            print('FLOW', reportparameter2str(r.flow), file=fid)
        if r.velocity is not None:
            print('VELOCITY', reportparameter2str(r.velocity), file=fid)
        if r.headloss is not None:
            print('HEADLOSS', reportparameter2str(r.headloss), file=fid)
        if r.setting is not None:
            print('SETTING', reportparameter2str(r.setting), file=fid)
        if r.reaction is not None:
            print('REACTION', reportparameter2str(r.reaction), file=fid)
        if r.ffactor is not None:
            print('F-FACTOR', reportparameter2str(r.ffactor), file=fid)
    if network.reportprecision is not None:
        r = network.reportprecision
        if r.elevation is not None:
            print('ELEVATION', reportprecision2str(r.elevation), file=fid)
        if r.demand is not None:
            print('DEMAND', reportprecision2str(r.demand), file=fid)
        if r.head is not None:
            print('HEAD', reportprecision2str(r.head), file=fid)
        if r.pressure is not None:
            print('PRESSURE', reportprecision2str(r.pressure), file=fid)
        if r.quality is not None:
            print('QUALITY', reportprecision2str(r.quality), file=fid)
        if r.length is not None:
            print('LENGTH', reportprecision2str(r.length), file=fid)
        if r.diameter is not None:
            print('DIAMETER', reportprecision2str(r.diameter), file=fid)
        if r.flow is not None:
            print('FLOW', reportprecision2str(r.flow), file=fid)
        if r.velocity is not None:
            print('VELOCITY', reportprecision2str(r.velocity), file=fid)
        if r.headloss is not None:
            print('HEADLOSS', reportprecision2str(r.headloss), file=fid)
        if r.position is not None:
            print('POSITION', reportprecision2str(r.position), file=fid)
        if r.setting is not None:
            print('SETTING', reportprecision2str(r.setting), file=fid)
        if r.reaction is not None:
            print('REACTION', reportprecision2str(r.reaction), file=fid)
        if r.ffactor is not None:
            print('F-FACTOR', reportparameter2str(r.ffactor), file=fid)
    print('\n', end=' ', file=fid)
