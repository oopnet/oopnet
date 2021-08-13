import datetime
from .decorators import section_reader
from ...elements.system_operation import Curve, Pattern, Energy, Control, Controlcondition, Action, Rule, Condition


@section_reader('CURVES', 0)
def read_curves(network, block):
    for vals in block:
        vals = vals['values']
        if vals[0] in list(network.networkhash['curve'].keys()):
            c = network.networkhash['curve'][vals[0]]
        else:
            c = Curve(id=vals[0])
            network.networkhash['curve'][vals[0]] = c
        if len(vals) > 1:
            m = float(vals[1])
            if c.xvalues is None:
                c.xvalues = m
            elif isinstance(c.xvalues, float):
                c.xvalues = list(c.xvalues).append(m)
            else:
                c.xvalues.append(m)
        if len(vals) > 2:
            m = float(vals[2])
            if c.yvalues is None:
                c.yvalues = m
            elif isinstance(c.yvalues, float):
                c.yvalues = list(c.yvalues).append(m)
            else:
                c.yvalues.append(m)
        if network.curves is None:
            network.curves = [c]
        else:
            if c not in network.curves:
                network.curves.append(c)


@section_reader('PATTERNS', 0)
def read_patterns(network, block):
    for vals in block:
        m = None
        vals = vals['values']
        if vals[0] in list(network.networkhash['pattern'].keys()):
            p = network.networkhash['pattern'][vals[0]]
        else:
            p = Pattern(id=vals[0])
            network.networkhash['pattern'][vals[0]] = p
        if len(vals) == 2:
            m = float(vals[1])
        elif len(vals) > 2:
            m = list(map(float, vals[1:]))
        if p.multipliers is None:
            p.multipliers = m
        elif len(p.multipliers) == 1:
            if isinstance(m, float):
                p.multipliers.append(m)
            else:
                for l in m:
                    p.multipliers.append(l)
        else:
            if isinstance(m, float):
                p.multipliers.append(m)
            else:
                for l in m:
                    p.multipliers.append(l)
        if network.patterns is None:
            network.patterns = [p]
        else:
            if p not in network.patterns:
                network.patterns.append(p)


@section_reader('ENERGY', 3)
def read_energy(network, block):
    for vals in block:
        vals = vals['values']
        e = Energy()
        if vals[0].upper() == 'GLOBAL':
            e.keyword = 'GLOBAL'
            e.parameter = vals[1].upper()
            if e.parameter == 'PATTERN':
                p = next(filter(lambda x: x.id==vals[2], network.patterns))
                e.value = p
            else:
                e.value = float(vals[2])
        elif vals[0].upper() == 'PUMP':
            e.keyword = 'PUMP'
            e.pumpid = network.networkhash['link'][vals[1]]
            e.parameter = vals[2].upper()
            if e.parameter == 'PATTERN':
                e.value = network.networkhash['pattern'][vals[3]]
            elif e.parameter.startswith('EFFIC'):
                e.value = network.networkhash['curve'][vals[3]]
            else:
                e.value = float(vals[3])
        elif vals[0].upper() == 'DEMAND' and vals[1].upper() == 'CHARGE':
            e.keyword = 'DEMAND CHARGE'
            e.value = float(vals[2])
        if network.energies is None:
            network.energies = [e]
        else:
            network.energies.append(e)


@section_reader('STATUS', 3)
def read_status(network, block):
    for vals in block:
        vals = vals['values']
        l = network.networkhash['link'][vals[0]]
        try:
            l.setting = float(vals[1])
        except:
            l.status = vals[1].upper()


@section_reader('CONTROLS', 3)
def read_controls(network, block):
    for vals in block:
        vals = vals['values']
        condition = Controlcondition()
        if vals[2].upper() == 'OPEN' or vals[2].upper() == 'CLOSED':
            action = Action(object=network.networkhash['link'][vals[1]], value=vals[2].upper())
        else:
            action = Action(object=network.networkhash['link'][vals[1]], value=float(vals[2]))
        if vals[3].upper() == 'IF':
            condition = Controlcondition(object=network.networkhash['node'][vals[5]], relation=vals[6].upper(),
                                         value=float(vals[7]))
        elif vals[3].upper() == 'AT':
            if vals[4].upper() == 'TIME':
                if ':' in vals[5]:
                    dt = vals[5].split(':')
                    condition = Controlcondition(time=datetime.timedelta(hours=float(dt[0]), minutes=float(dt[1])))
                else:
                    condition = Controlcondition(time=datetime.timedelta(hours=float(vals[5])))
            elif vals[4].upper() == 'CLOCKTIME':
                if len(vals) == 6:
                    timeformat = '%H:%M'
                    condition = Controlcondition(clocktime=datetime.datetime.strptime(vals[5], timeformat))
                elif len(vals) == 7:
                    if ':' in vals[5]:
                        timeformat = '%I:%M%p'
                    else:
                        timeformat = '%I%p'
                    condition = Controlcondition(clocktime=datetime.datetime.strptime(vals[5] + vals[6],
                                                                                      timeformat))
        c = Control(action=action, condition=condition)
        if network.controls is None:
            network.controls = [c]
        else:
            network.controls.append(c)


@section_reader('RULES', 0)
def read_rules(network, block):
    for vals in block:
        vals = vals['values']
        if vals[0].upper() == 'RULE':
            r = Rule(id=vals[1])
            if network.rules is None:
                network.rules = [r]
            else:
                network.rules.append(r)
        else:
            if vals[0].upper() == 'PRIORITY':
                r.priority = float(vals[1])
            else:
                ac = Condition(logical=vals[0].upper())
                if vals[2] in list(network.networkhash['link'].keys()):
                    ac.object = network.networkhash['link'][vals[2]]
                    ac.attribute = vals[3].upper()
                    ac.relation = vals[4].upper()
                    try:
                        ac.value = float(vals[5])
                    except:
                        ac.value = vals[5].upper()
                elif vals[2] in list(network.networkhash['node'].keys()):
                    ac.object = network.networkhash['node'][vals[2]]
                    ac.attribute = vals[3].upper()
                    ac.relation = vals[4].upper()
                    try:
                        ac.value = float(vals[5])
                    except:
                        ac.value = vals[5].upper()
                elif vals[1].upper() == 'SYSTEM':
                    ac.attribute = vals[2].upper()
                    ac.relation = vals[3].upper()
                    if ac.attribute == 'TIME':
                        if ':' in vals[4]:
                            dt = vals[4].split(':')
                            ac.value = datetime.timedelta(hours=float(dt[0]), minutes=float(dt[1]))
                        else:
                            ac.value = datetime.timedelta(hours=float(vals[4]))
                    elif ac.attribute == 'CLOCKTIME':
                        if len(vals) == 5:
                            if ':' in vals[4]:
                                timeformat = '%H:%M'
                            else:
                                timeformat = '%H'
                            ac.value = datetime.datetime.strptime(vals[4], timeformat)
                        if len(vals) == 6:
                            if ':' in vals[4]:
                                timeformat = '%I:%M%p'
                            else:
                                timeformat = '%I%p'
                            ac.value = datetime.datetime.strptime(vals[4] + vals[5], timeformat)
                    else:
                        try:
                            ac.value = float(vals[4])
                        except:
                            ac.value = vals[4].upper()
                if r.condition is None:
                    r.condition = [ac]
                else:
                    r.condition.append(ac)


@section_reader('DEMANDS', 2)
def read_demands(network, block):
    for vals in block:
        vals = vals['values']
        j = network.networkhash['node'][vals[0]]
        if len(vals) > 1:
            if j.demand:
                j.demand = float(vals[1])
            elif isinstance(j.demand, float):
                if abs(j.demand) > 0.0:
                    j.demand = [j.demand, float(vals[1])]
                else:
                    j.demand = float(vals[1])
            elif isinstance(j.demand, list):
                j.demand.append(float(vals[1]))
        if len(vals) > 2:
            p = network.networkhash['pattern'][vals[2]]
            if j.demandpattern is None:
                j.demandpattern = p
            elif isinstance(j.demandpattern, Pattern):
                j.demandpattern = [j.demandpattern, p]
            else:
                j.demandpattern.append(p)
