import datetime
from .decorators import section_writer
from ...elements.system_operation import Curve
from ...elements.network_components import Junction, Reservoir, Tank, Pipe, Valve, Pump


@section_writer('CURVES', 3)
def write_curves(network, fid):
    print('[CURVES]', file=fid)
    print(';id xvalue yvalue', file=fid)
    if network.curves is not None:
        for c in network.curves:
            for x, y in zip(c.xvalues, c.yvalues):
                print(c.id, x, y, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('PATTERNS', 3)
def write_patterns(network, fid):
    print('[PATTERNS]', file=fid)
    print(';id multipliers', file=fid)
    if network.patterns is not None:
        for p in network.patterns:
            for i, m in enumerate(p.multipliers):
                print(p.id, end=' ', file=fid)
                print(m, file=fid)
            print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('ENERGY', 3)
def write_energy(network, fid):
    print('[ENERGY]', file=fid)
    if network.energies is not None:
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
def write_status(network, fid):
    print('[STATUS]', file=fid)
    print(';id status/setting', file=fid)
    for key in list(network.networkhash['link'].keys()):
        l = network.networkhash['link'][key]
        if l.initialstatus is not None:
            print(l.id, l.initialstatus, file=fid)
        elif l.setting is not None:
            if l.setting == 0:
                print(l.id, 'OPEN', file=fid)
            elif l.setting == 1:
                print(l.id, 'CLOSED', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('CONTROLS', 3)
def write_controls(network, fid):
    print('[CONTROLS]', file=fid)
    if network.controls is not None:
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
def write_rules(network, fid):
    print('[RULES]', file=fid)
    if network.rules is not None:
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
def write_demands(network, fid):
    print('[DEMANDS]', file=fid)
    print(';id demand pattern category', file=fid)
    if network.junctions is not None:
        for j in network.junctions:
            if j.demand is None:
                pass
            elif isinstance(j.demand, float):
                pass
            elif isinstance(j.demand, list):
                for i, d in enumerate(j.demand):
                    if i != 0:
                        print(j.id, end=' ', file=fid)
                        print(d, end=' ', file=fid)
                        try:
                            print(j.demandpattern[i].id, end=' ', file=fid)
                        except:
                            pass
                        print('\n', end=' ', file=fid)
            else:
                print('unknown demand dtype')
    print('\n', end=' ', file=fid)
