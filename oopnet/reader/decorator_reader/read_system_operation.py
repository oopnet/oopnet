import datetime

from oopnet.elements.base import PipeStatus, PumpStatus, ValveStatus, EnergyKeyword, EnergyParameter, Relation, \
    LimitSetting, Logic, ConditionAttribute
from oopnet.elements.network import Network
from oopnet.elements.network_components import Pipe, Pump
from oopnet.elements.system_operation import Curve, Pattern, Energy, Control, Controlcondition, Action, Rule, Condition
from oopnet.utils.getters.get_by_id import get_curve, get_pump, get_pattern, get_link, get_node, get_junction
from oopnet.utils.getters.element_lists import get_link_ids, get_node_ids, get_curve_ids, get_pattern_ids
from oopnet.reader.decorator_reader.decorators import section_reader
from oopnet.utils.adders import add_curve, add_pattern, add_rule


@section_reader('CURVES', 0)
def read_curves(network: Network, block: list):
    """Reads curves from block.

    Args:
      network: OOPNET network object where the curves shall be stored
      block: EPANET input file block
    """
    for vals in block:
        vals = vals['values']
        exists = False

        if vals[0] in get_curve_ids(network):
            c = get_curve(network, vals[0])
            exists = True
        else:
            c = Curve(id=vals[0])

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

        if not exists:
            add_curve(network, c, False)


@section_reader('PATTERNS', 0)
def read_patterns(network: Network, block: list):
    """Reads patterns from block.

    Args:
      network: OOPNET network object where the patterns shall be stored
      block: EPANET input file block
    """
    for vals in block:
        m = None
        vals = vals['values']

        exists = False

        if vals[0] in get_pattern_ids(network):
            p = get_pattern(network, vals[0])
            exists = True
        else:
            p = Pattern(id=vals[0])

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
        if not exists:
            add_pattern(network, p, False)


@section_reader('ENERGY', 3)
def read_energy(network: Network, block: list):
    """Reads energy from block.

    Args:
      network: OOPNET network object where the energy curves shall be stored
      block: EPANET input file block
    """
    for vals in block:
        vals = vals['values']
        e = Energy()
        if vals[0].upper() == 'GLOBAL':
            e.keyword = EnergyKeyword[vals[0].upper()]
            param = 'EFFICIENCY' if 'EFF' in vals[1].upper() else vals[1].upper()
            e.parameter = EnergyParameter(param)
            if e.parameter == EnergyParameter.PATTERN:
                p = get_pattern(network, vals[2])
                e.value = p
            else:
                e.value = float(vals[2])
        elif vals[0].upper() == 'PUMP':
            e.keyword = EnergyKeyword[vals[0].upper()]
            e.pumpid = get_pump(network, vals[1])
            e.parameter = EnergyParameter[vals[2].upper()]
            if e.parameter == EnergyParameter.PATTERN:
                e.value = get_pattern(network, vals[3])
            elif e.parameter == EnergyParameter.EFFICIENCY:
                e.value = get_curve(network, vals[3])
            else:
                e.value = float(vals[3])
        elif vals[0].upper() == 'DEMAND' and vals[1].upper() == 'CHARGE':
            e.keyword = EnergyParameter['DEMAND_CHARGE']
            e.value = float(vals[2])
        # todo: create add function
        if network.energies is None:
            network.energies = [e]
        else:
            network.energies.append(e)


@section_reader('STATUS', 3)
def read_status(network: Network, block: list):
    """Reads status information from block.

    Args:
      network: OOPNET network object where the status information shall be stored
      block: EPANET input file block

    """
    for vals in block:
        vals = vals['values']
        l = get_link(network, vals[0])
        try:
            # todo: necessary? cast to roughness or equivalent possible?
            l.setting = float(vals[1])
        except:
            status = vals[1].upper()
            if isinstance(l, Pipe):
                l.status = PipeStatus(status)
            elif isinstance(l, Pump):
                l.status = PumpStatus(status)
            else:
                l.status = ValveStatus(status)


@section_reader('CONTROLS', 3)
def read_controls(network: Network, block: list):
    """Reads controls from block.

    Args:
      network: OOPNET network object where the controls shall be stored
      block: EPANET input file block

    """
    for vals in block:
        vals = vals['values']
        condition = Controlcondition()
        if vals[2].upper() in ['OPEN', 'CLOSED']:
            l = get_link(network, vals[1])
            action = Action(object=l, value=vals[2].upper())
        else:
            l = get_link(network, vals[1])
            action = Action(object=l, value=float(vals[2]))
        if vals[3].upper() == 'IF':
            n = get_node(network, vals[5])
            condition = Controlcondition(object=n, relation=LimitSetting[vals[6].upper()], value=float(vals[7]))
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
                    timeformat = '%I:%M%p' if ':' in vals[5] else '%I%p'
                    condition = Controlcondition(clocktime=datetime.datetime.strptime(vals[5] + vals[6],
                                                                                      timeformat))
        c = Control(action=action, condition=condition)
        # todo: create adder function
        if network.controls is None:
            network.controls = [c]
        else:
            network.controls.append(c)


@section_reader('RULES', 0)
def read_rules(network: Network, block: list):
    """Reads rules from block.

    Args:
      network: OOPNET network object where the rules shall be stored
      block: EPANET input file block

    """
    for vals in block:
        vals = vals['values']
        if vals[0].upper() == 'RULE':
            r = Rule(id=vals[1])
            add_rule(network, r)
        else:
            if vals[0].upper() == 'PRIORITY':
                r.priority = float(vals[1])
            else:
                ac = Condition(logical=Logic[vals[0].upper()])
                if vals[2] in get_link_ids(network):
                    l = get_link(network, vals[2])
                    ac.object = l
                    ac.attribute = ConditionAttribute[vals[3].upper()]
                    ac.relation = Relation.parse(vals[4].upper())
                    try:
                        ac.value = float(vals[5])
                    except:
                        ac.value = vals[5].upper()
                elif vals[2] in get_node_ids(network):
                    n = get_node(network, vals[2])
                    ac.object = n
                    ac.attribute = ConditionAttribute[vals[3].upper()]
                    ac.relation = Relation.parse(vals[4].upper())
                    try:
                        ac.value = float(vals[5])
                    except:
                        ac.value = vals[5].upper()
                elif vals[1].upper() == 'SYSTEM':
                    ac.attribute = ConditionAttribute[vals[2].upper()]
                    ac.relation = Relation.parse(vals[3].upper())
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
                # todo: create adder function
                if r.condition is None:
                    r.condition = [ac]
                else:
                    r.condition.append(ac)


@section_reader('DEMANDS', 2)
def read_demands(network: Network, block: list):
    """Reads demands from block.

    Args:
      network: OOPNET network object where the demands shall be stored
      block: EPANET input file block

    """
    for vals in block:
        vals = vals['values']
        j = get_junction(network, vals[0])
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
            p = get_pattern(network, vals[2])
            if j.demandpattern is None:
                j.demandpattern = p
            elif isinstance(j.demandpattern, Pattern):
                j.demandpattern = [j.demandpattern, p]
            else:
                j.demandpattern.append(p)
