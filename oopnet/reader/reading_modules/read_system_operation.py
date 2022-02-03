from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
import logging

from oopnet.elements.system_operation import Curve, Pattern
from oopnet.elements.system_operation import Energy, Control, Controlcondition, Action, Rule, Condition
from oopnet.utils.getters import get_curve, get_pump, get_pattern, get_link, get_node, get_junction, get_link_ids, \
    get_node_ids, get_curve_ids, get_pattern_ids
from oopnet.reader.decorators import section_reader
from oopnet.utils.adders import add_curve, add_pattern, add_rule
if TYPE_CHECKING:
    from oopnet.elements import Network


logger = logging.getLogger(__name__)


@section_reader('CURVES', 0)
def read_curves(network: Network, block: list):
    """Reads curves from block.

    Args:
      network: OOPNET network object where the curves shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading Curves')
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
            add_curve(network, c)


@section_reader('PATTERNS', 0)
def read_patterns(network: Network, block: list):
    """Reads patterns from block.

    Args:
      network: OOPNET network object where the patterns shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading Patterns')
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
        if (
            p.multipliers is not None
            and len(p.multipliers) == 1
            and isinstance(m, float)
            or p.multipliers is not None
            and len(p.multipliers) != 1
            and isinstance(m, float)
        ):
            p.multipliers.append(m)
        elif (
            p.multipliers is not None
            and len(p.multipliers) == 1
            or p.multipliers is not None
        ):
            for l in m:
                p.multipliers.append(l)
        else:
            p.multipliers = m
        if not exists:
            add_pattern(network, p)


@section_reader('ENERGY', 3)
def read_energy(network: Network, block: list):
    """Reads energy from block.

    Args:
      network: OOPNET network object where the energy curves shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading Energy')
    for vals in block:
        vals = vals['values']
        e = Energy()
        if vals[0].upper() == 'GLOBAL':
            e.keyword = vals[0].upper()
            param = 'EFFICIENCY' if 'EFF' in vals[1].upper() else vals[1].upper()
            e.parameter = param
            if e.parameter == 'PATTERN':
                p = get_pattern(network, vals[2])
                e.value = p
            else:
                e.value = float(vals[2])
        elif vals[0].upper() == 'PUMP':
            e.keyword = vals[0].upper()
            e.pumpid = get_pump(network, vals[1])
            param = 'EFFICIENCY' if 'EFF' in vals[2].upper() else vals[2].upper()
            e.parameter = param
            if e.parameter == 'PATTERN':
                e.value = get_pattern(network, vals[3])
            elif e.parameter == 'EFFICIENCY':
                e.value = get_curve(network, vals[3])
            else:
                e.value = float(vals[3])
        elif vals[0].upper() == 'DEMAND' and vals[1].upper() == 'CHARGE':
            e.keyword = 'DEMAND_CHARGE'
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
    logger.debug('Reading status section')
    for vals in block:
        vals = vals['values']
        l = get_link(network, vals[0])
        try:
            # todo: necessary? cast to roughness or equivalent possible?
            l.setting = float(vals[1])
        except:
            l.status = vals[1].upper()


@section_reader('CONTROLS', 3)
def read_controls(network: Network, block: list):
    """Reads controls from block.

    Args:
      network: OOPNET network object where the controls shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading Controls')
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
            condition = Controlcondition(object=n, relation=vals[6].upper(), value=float(vals[7]))
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
        # todo: create adder function for controls
        if network.controls is None:
            network.controls = [c]
        else:
            network.controls.append(c)


@section_reader('RULES', 3)
def read_rules(network: Network, block: list):
    """Reads rules from block.

    Args:
      network: OOPNET network object where the rules shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading Rules')
    for vals in block:
        vals = vals['values']
        if vals[0].upper() == 'RULE':
            r = Rule(id=vals[1])
            add_rule(network, r)
        elif vals[0].upper() == 'PRIORITY':
            r.priority = float(vals[1])
        else:
            ac = Condition(logical=vals[0].upper())
            if vals[2] in get_link_ids(network):
                l = get_link(network, vals[2])
                ac.object = l
                ac.attribute = vals[3].upper()
                ac.relation = vals[4].upper()
                try:
                    ac.value = float(vals[5])
                except:
                    ac.value = vals[5].upper()
            elif vals[2] in get_node_ids(network):
                n = get_node(network, vals[2])
                ac.object = n
                ac.attribute = vals[3].upper()
                ac.relation = vals[4].upper()
                try:
                    ac.value = float(vals[5])
                except:
                    ac.value = vals[5].upper()
            elif vals[1].upper() == 'SYSTEM':
                ac.object = 'SYSTEM'
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
                        timeformat = '%H:%M' if ':' in vals[4] else '%H'
                        ac.value = datetime.datetime.strptime(vals[4], timeformat)
                    if len(vals) == 6:
                        timeformat = '%I:%M%p' if ':' in vals[4] else '%I%p'
                        ac.value = datetime.datetime.strptime(vals[4] + vals[5], timeformat)
                else:
                    try:
                        ac.value = float(vals[4])
                    except:
                        ac.value = vals[4].upper()
            # todo: create adder function for conditions
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
    logger.debug('Reading demand section')
    for vals in block:
        vals = vals['values']
        j = get_junction(network, vals[0])
        if len(vals) > 1:
            if (
                not j.demand
                and isinstance(j.demand, float)
                and abs(j.demand) > 0.0
            ):
                j.demand = [j.demand, float(vals[1])]
            elif not j.demand and isinstance(j.demand, float) or j.demand:
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
