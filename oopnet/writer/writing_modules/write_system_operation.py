from __future__ import annotations
from typing import TYPE_CHECKING
import datetime
from io import TextIOWrapper
import logging

from oopnet.elements.base import NetworkComponent
from oopnet.elements.system_operation import Curve, Pattern
from oopnet.utils.getters.element_lists import get_curves, get_junctions, get_pipes, get_valves, get_pumps, \
    get_patterns, get_energy_entries, get_controls, get_rules
from oopnet.writer.decorators import section_writer
if TYPE_CHECKING:
    from oopnet.elements.network import Network

logger = logging.getLogger(__name__)


@section_writer('CURVES', 3)
def write_curves(network: Network, fid: TextIOWrapper):
    """Writes curves to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Curves section')
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
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Patterns section')
    print('[PATTERNS]', file=fid)
    print(';id multipliers', file=fid)
    for p in get_patterns(network):
        for m in p.multipliers:
            print(p.id, end=' ', file=fid)
            print(m, file=fid)
        print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('ENERGY', 3)
def write_energy(network: Network, fid: TextIOWrapper):
    """Writes energy section to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Energy section')
    print('[ENERGY]', file=fid)
    for e in get_energy_entries(network):
        keyword = e.keyword if e.keyword != 'DEMAND_CHARGE' else 'DEMAND CHARGE'
        print(keyword, end=' ', file=fid)
        if keyword == 'PUMP':
            print(e.pumpid.id, end=' ', file=fid)
        if e.parameter is not None:
            print(e.parameter, end=' ', file=fid)
        if e.value is not None:
            if isinstance(e.value, (Curve, Pattern)):
                print(e.value.id, end=' ', file=fid)
            else:
                print(e.value, end=' ', file=fid)
            print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('STATUS', 3)
def write_status(network: Network, fid: TextIOWrapper):
    """Writes status section to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Status section')
    print('[STATUS]', file=fid)
    print(';id status/setting', file=fid)
    for l in get_pipes(network):
        if l.status == 'CLOSED':
            print(l.id, l.status, file=fid)
    for v in get_valves(network):
        if v.status == 'CLOSED' or v.setting == 1:
            print(v.id, v.status, file=fid)
    for pu in get_pumps(network):
        if pu.status == 'CLOSED':
            print(pu.id, pu.status, file=fid)
        # elif pu.keyword == 'SPEED':
        #     print(pu.id, pu, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('CONTROLS', 3)
def write_controls(network: Network, fid: TextIOWrapper):
    """Writes controls section to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Controls section')
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
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Rules section')
    print('[RULES]', file=fid)
    for r in get_rules(network):
        print('RULE', r.id, file=fid)
        for c in r.condition:
            if isinstance(c.object, NetworkComponent):
                object_type = c.object.__class__.__name__
                print(c.logical, object_type, c.object.id, c.attribute, c.relation, c.value, file=fid)
            elif c.attribute is not None:
                object_type = 'SYSTEM'
                if c.attribute == 'TIME':
                    print(c.logical, object_type, c.attribute, c.relation, str(c.value)[:-3], file=fid)
                elif c.attribute == 'CLOCKTIME':
                    timeformat = '%I:%M %p'
                    print(c.logical, object_type, c.attribute, c.relation, \
                          datetime.datetime.strftime(c.value, timeformat), file=fid)
    print('\n', end=' ', file=fid)


@section_writer('DEMANDS', 3)
def write_demands(network: Network, fid: TextIOWrapper):
    """Writes the demand section to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Demands section')
    print('[DEMANDS]', file=fid)
    print(';id demand pattern category', file=fid)
    for j in get_junctions(network):
        if j.demand is None or isinstance(j.demand, float) or isinstance(j.demand, int):
            pass
        elif isinstance(j.demand, list):
            for i, d in enumerate(j.demand):
                if i == 0:  # skip first line
                    continue
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
