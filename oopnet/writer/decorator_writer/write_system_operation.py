import datetime
from io import TextIOWrapper

from oopnet.elements.system_operation import Curve
from oopnet.elements.network_components import Junction, Reservoir, Tank, Pipe, Valve, Pump
from oopnet.elements.network import Network

from .decorators import section_writer


@section_writer('CURVES', 3)
def write_curves(network: Network, fid: TextIOWrapper):
    """Writes curves to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[CURVES]', file=fid)
    print(';id xvalue yvalue', file=fid)
    for c in network.curves:
        for x, y in zip(c.xvalues, c.yvalues):
            print(c.id, x, y, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('PATTERNS', 3)
def write_patterns(network: Network, fid: TextIOWrapper):
    """Writes patterns to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[PATTERNS]', file=fid)
    print(';id multipliers', file=fid)
    for p in network.patterns:
        for i, m in enumerate(p.multipliers):
            print(p.id, end=' ', file=fid)
            print(m, file=fid)
        print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('ENERGY', 3)
def write_energy(network: Network, fid: TextIOWrapper):
    """Writes energy section to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[ENERGY]', file=fid)
    for e in network.energies:
        print(e.keyword, end=' ', file=fid)
        if e.keyword == 'PUMP':
            print(e.pumpid.id, end=' ', file=fid)
        if e.parameter is not None:
            print(e.parameter, end=' ', file=fid)
        if e.value is not None:
            if isinstance(e.value, Curve):
                print(e.value.id, end=' ', file=fid)
            else:
                print(e.value, end=' ', file=fid)
            print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('STATUS', 3)
def write_status(network: Network, fid: TextIOWrapper):
    """Writes status section to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[STATUS]', file=fid)
    print(';id status/setting', file=fid)
    for l in network.pipes:
        if l.initialstatus == 'CLOSED':
            print(l.id, l.initialstatus, file=fid)
    for v in network.valves:
        if v.initialstatus == 'CLOSED' or v.setting == 1:
            print(v.id, 'CLOSED', file=fid)
    for pu in network.pumps:
        if pu.initialstatus == 'CLOSED':
            print(pu.id, 'CLOSED', file=fid)
        elif pu.keyword == 'SPEED':
            print(pu.id, pu.value, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('CONTROLS', 3)
def write_controls(network: Network, fid: TextIOWrapper):
    """Writes controls section to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[CONTROLS]', file=fid)
    for c in network.controls:
        print('LINK', c.action.object.id, c.action.value, end=' ', file=fid)
        if c.condition.object is not None:
            print('IF NODE', c.condition.object.id, c.condition.relation, c.condition.value, file=fid)
        elif c.condition.time is not None:
            print('AT TIME', str(c.condition.time)[:-3], file=fid)
        elif c.condition.clocktime is not None:
            print('AT CLOCKTIME', datetime.datetime.strftime(c.condition.clocktime, '%I:%M %p'), file=fid)
    print('\n', end=' ', file=fid)


@section_writer('RULES', 3)
def write_rules(network: Network, fid: TextIOWrapper):
    """Writes rules to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[RULES]', file=fid)
    for r in network.rules:
        print('RULE', r.id, file=fid)
        for c in r.condition:
            objecttype = None
            if c.object is not None:
                if isinstance(c.object, Junction):
                    objecttype = 'JUNCTION'
                elif isinstance(c.object, Reservoir):
                    objecttype = 'RESERVOIR'
                elif isinstance(c.object, Tank):
                    objecttype = 'TANK'
                elif isinstance(c.object, Pipe):
                    objecttype = 'PIPE'
                elif isinstance(c.object, Valve):
                    objecttype = 'VALVE'
                elif isinstance(c.object, Pump):
                    objecttype = 'PUMP'
                print(c.logical, objecttype, c.object.id, c.attribute, c.relation, c.value, file=fid)
            elif c.attribute is not None:
                objecttype = 'SYSTEM'
                if c.attribute == 'TIME':
                    print(c.logical, objecttype, c.attribute, c.relation, str(c.value)[:-3], file=fid)
                elif c.attribute == 'CLOCKTIME':
                    timeformat = '%I:%M %p'
                    print(c.logical, objecttype, c.attribute, c.relation, \
                          datetime.datetime.strftime(c.value, timeformat), file=fid)
    print('\n', end=' ', file=fid)


@section_writer('DEMANDS', 3)
def write_demands(network: Network, fid: TextIOWrapper):
    """Writes the demand section to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[DEMANDS]', file=fid)
    print(';id demand pattern category', file=fid)
    for j in network.junctions:
        if j.demand is None or isinstance(j.demand, float) or isinstance(j.demand, int):
            pass
        elif isinstance(j.demand, list):
            for i, d in enumerate(j.demand):
                if i != 0:
                    print(j.id, end=' ', file=fid)
                    print(d, end=' ', file=fid)
                    # todo: replace try except
                    try:
                        print(j.demandpattern[i].id, end=' ', file=fid)
                    except:
                        pass
                    print('\n', end=' ', file=fid)
        else:
            raise TypeError(f'Unknown demand dtype {type(j.demand)}')
    print('\n', end=' ', file=fid)
