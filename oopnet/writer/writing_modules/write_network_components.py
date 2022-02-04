from __future__ import annotations
from typing import TYPE_CHECKING
from io import TextIOWrapper
import logging

from oopnet.elements.system_operation import Curve
from oopnet.utils.getters.element_lists import get_junctions, get_reservoirs, get_tanks, get_pipes, get_pumps, \
    get_valves
from oopnet.writer.decorators import section_writer
if TYPE_CHECKING:
    from oopnet.elements.network import Network

logger = logging.getLogger(__name__)


@section_writer('TITLE', 0)
def write_title(network: Network, fid: TextIOWrapper):
    """Writes the Network title to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing title')
    print('[TITLE]', file=fid)
    if network.title:
        print(network.title, file=fid)
    print('\n', file=fid)


@section_writer('JUNCTIONS', 1)
def write_junctions(network: Network, fid: TextIOWrapper):
    """Writes Junctions to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Junctions section')
    print('[JUNCTIONS]', file=fid)
    print(';id elevation demand demandpattern', file=fid)
    for j in get_junctions(network):
        print(j.id, end=' ', file=fid)
        print(j.elevation, end=' ', file=fid)
        if isinstance(j.demand, list):
            print(j.demand[0], end=' ', file=fid)
        else:
            print(j.demand, end=' ', file=fid)
        if j.demandpattern is not None:
            if isinstance(j.demandpattern, list):
                print(j.demandpattern[0].id, end=' ', file=fid)
            else:
                print(j.demandpattern.id, end=' ', file=fid)
        if j.comment is not None:
            print(';', j.comment, end=' ', file=fid)
        print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('RESERVOIRS', 1)
def write_reservoirs(network: Network, fid: TextIOWrapper):
    """Writes Reservoirs to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Reservoirs section')
    print('[RESERVOIRS]', file=fid)
    print(';id head pattern', file=fid)
    for r in get_reservoirs(network):
        print(r.id, end=' ', file=fid)
        print(r.head, end=' ', file=fid)
        if r.headpattern is not None:
            print(r.headpattern.id, end=' ', file=fid)
        if r.comment is not None:
            print(';', r.comment, end=' ', file=fid)
        print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('TANKS', 1)
def write_tanks(network: Network, fid: TextIOWrapper):
    """Writes tanks to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Tanks section')
    print('[TANKS]', file=fid)
    print(';id elevation initlevel minlevel maxlevel diam minvolume volumecurve', file=fid)
    for t in get_tanks(network):
        print(t.id, end=' ', file=fid)
        print(t.elevation, end=' ', file=fid)
        print(t.initlevel, end=' ', file=fid)
        print(t.minlevel, end=' ', file=fid)
        print(t.maxlevel, end=' ', file=fid)
        print(t.diam, end=' ', file=fid)
        if t.minvolume is not None:
            print(t.minvolume, end=' ', file=fid)
        if t.volumecurve is not None:
            print(t.volumecurve, end=' ', file=fid)
        if t.comment is not None:
            print(';', t.comment, end=' ', file=fid)
        print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('PIPES', 2)
def write_pipes(network: Network, fid: TextIOWrapper):
    """Writes pipes to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Pipes section')
    print('[PIPES]', file=fid)
    print(';id startnode endnode length diameter roughness minorloss', file=fid)  # status', file=fid)
    for p in get_pipes(network):
        print(p.id, end=' ', file=fid)
        if p.startnode is not None:
            print(p.startnode.id, end=' ', file=fid)
        if p.endnode is not None:
            print(p.endnode.id, end=' ', file=fid)
        print(p.length, end=' ', file=fid)
        print(p.diameter, end=' ', file=fid)
        print(p.roughness, end=' ', file=fid)
        print(p.minorloss, end=' ', file=fid)
        if p.status == 'CV':
            print(p.status, end=' ', file=fid)
        if p.comment is not None:
            print(';', p.comment, end=' ', file=fid)
        print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('PUMPS', 2)
def write_pumps(network: Network, fid: TextIOWrapper):
    """Writes pumps to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Pumps section')
    print('[PUMPS]', file=fid)
    print(';id startnode endnode keyword value', file=fid)
    for p in get_pumps(network):
        print(p.id, end=' ', file=fid)
        if p.startnode is not None:
            print(p.startnode.id, end=' ', file=fid)
        if p.endnode is not None:
            print(p.endnode.id, end=' ', file=fid)
        if p.power is not None:
            print('POWER', p.power, end=' ', file=fid)
        if p.head is not None:
            print('HEAD', p.head.id, end=' ', file=fid)
        if p.speed is not None:
            print('SPEED', p.speed, end=' ', file=fid)
        if p.pattern is not None:
            print('PATTERN', p.pattern.id, end=' ', file=fid)
        if p.comment is not None:
            print(';', p.comment, end=' ', file=fid)
        print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('VALVES', 2)
def write_valves(network: Network, fid: TextIOWrapper):
    """Writes valves to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Valves section')
    print('[VALVES]', file=fid)
    print(';id startnode endnode diameter valvetype setting minorloss', file=fid)
    for v in get_valves(network):
        print(v.id, end=' ', file=fid)
        if v.startnode is not None:
            print(v.startnode.id, end=' ', file=fid)
        if v.endnode is not None:
            print(v.endnode.id, end=' ', file=fid)
        print(v.diameter, end=' ', file=fid)
        print(v.__class__.__name__, end=' ', file=fid)
        if isinstance(v.setting, Curve):
            print(v.setting.id, end=' ', file=fid)
        else:
            print(v.setting, end=' ', file=fid)
        print(v.minorloss, end=' ', file=fid)
        if v.comment is not None:
            print(';', v.comment, end=' ', file=fid)
        print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('EMITTERS', 3)
def write_emitter(network: Network, fid: TextIOWrapper):
    """Writes Junction emitters to an EPANET input file.

    Args:
      network: Network object to write
      fid: output object

    """
    logger.debug('Writing Emitter section')
    print('[EMITTERS]', file=fid)
    print(';id emittercoefficient', file=fid)
    for j in get_junctions(network):
        if j.emittercoefficient > 0.0:
            print(j.id, j.emittercoefficient, file=fid)
    print('\n', file=fid)
