import datetime
from io import TextIOWrapper

from oopnet.elements.base import PipeStatus, ValveStatus, PumpStatus, EnergyKeyword, NetworkComponent, \
    ConditionAttribute
from oopnet.elements.system_operation import Curve
from oopnet.elements.network_components import Junction, Reservoir, Tank, Pipe, Valve, Pump
from oopnet.elements.network import Network
from oopnet.utils.getters.element_lists import get_curves, get_junctions, get_pipes, get_valves, get_pumps, \
    get_patterns, get_energies, get_controls, get_rules
from oopnet.writer.decorator_writer.decorators import section_writer


@section_writer('CURVES', 3)
def write_curves(network: Network, fid: TextIOWrapper):
    """Writes curves to an EPANET input file.

    Args:
      network: OOPNET network object to write
      fid: output object

    """
    print('[CURVES]', file=fid)
    print(';id xvalue yvalue', file=fid)
    for c in get_curves(network):
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
    for p in get_patterns(network):
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
    for e in get_energies(network):
        print(e.keyword.value, end=' ', file=fid)
        if e.keyword == EnergyKeyword.PUMP:
            print(e.pumpid.id, end=' ', file=fid)
        if e.parameter is not None:
            print(e.parameter.value, end=' ', file=fid)
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
    for l in get_pipes(network):
        if l.initialstatus == PipeStatus.CLOSED:
            print(l.id, l.initialstatus.name, file=fid)
    for v in get_valves(network):
        if v.initialstatus == ValveStatus.CLOSED or v.setting == 1:
            print(v.id, v.initialstatus.name, file=fid)
    for pu in get_pumps(network):
        if pu.initialstatus == PumpStatus.CLOSED:
            print(pu.id, pu.initialstatus.name, file=fid)
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
    for c in get_controls(network):
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
    for r in get_rules(network):
        print('RULE', r.id, file=fid)
        for c in r.condition:
            if isinstance(c.object, NetworkComponent):
                object_type = c.object.__class__.__name__
                print(c.logical.value, object_type, c.object.id, c.attribute.value, c.relation.value, c.value, file=fid)
            elif c.attribute is not None:
                object_type = 'SYSTEM'
                if c.attribute == ConditionAttribute.TIME:
                    print(c.logical.value, object_type, c.attribute.value, c.relation.value, str(c.value)[:-3], file=fid)
                elif c.attribute == ConditionAttribute.CLOCKTIME:
                    timeformat = '%I:%M %p'
                    print(c.logical.value, object_type, c.attribute.value, c.relation.value, \
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
    for j in get_junctions(network):
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
