from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from oopnet.reader.decorators import section_reader
from oopnet.reader.factories.component_factory import ComponentFactory
from oopnet.reader.factories.base import InvalidValveTypeError
from oopnet.elements.system_operation import Pattern, Curve
from oopnet.elements.network_components import Tank, Reservoir, Pipe, Pump, Valve, Node, Junction, TCV,\
    FCV, PRV, PBV, PSV, GPV
from oopnet.utils.getters.element_lists import get_junctions, get_reservoirs, get_tanks, get_pipes, get_valves, \
    get_pumps
from oopnet.utils.adders.add_element import add_junction, add_tank, add_reservoir, add_pipe, add_pump, add_valve
if TYPE_CHECKING:
    from oopnet.elements.network import Network


logger = logging.getLogger(__name__)


@section_reader('TITLE', 4)
def read_title(network: Network, block: list):
    """Reads the network title from block.

    Args:
      network: OOPNET network object where the title shall be stored
      block: EPANET input file block

    """
    logger.debug('Reading title')
    for vals in block:
        vals = vals['values']
        network.title = " ".join(vals)


@section_reader('EMITTERS', 4)
class EmitterFactory(ComponentFactory):
    """Factory for parsing and setting the emitter coefficients of Junctions."""
    def __new__(cls, network: Network, block: dict):
        logger.debug('Reading Emitters section')
        for values in block:
            junction, emittercoefficient = cls._parse_single(values, network)
            junction.emittercoefficient = emittercoefficient

    @classmethod
    def _parse_single(cls, values, network) -> tuple:
        attr_values = cls._pad_list(values['values'], 2)
        attr_names = ['junction', 'emittercoefficient']
        attr_cls = [Node, float]
        attr_dict = cls._create_attr_dict(attr_names, attr_values, attr_cls, network)
        return tuple(attr_dict[attr_name] for attr_name in attr_names)


@section_reader('JUNCTIONS', 1)
class JunctionFactory(ComponentFactory):
    """Factory for parsing and creating Junctions and adding them to a Network."""
    def __new__(cls, network: Network, block: dict):
        logger.debug('Reading Junctions section')
        for values in block:
            j = cls._parse_single(values, network)
            add_junction(network, j)
        logger.debug(f'Added {len(get_junctions(network))} Junctions')

    @classmethod
    def _parse_single(cls, values, network) -> Junction:
        comment = cls._read_comment(values)
        attr_values = cls._pad_list(values['values'], 4)
        attr_names = ['id', 'elevation', 'demand', 'demandpattern']
        attr_cls = [str, float, float, Pattern]
        attr_dict = cls._create_attr_dict(attr_names, attr_values, attr_cls, network)
        return Junction(**attr_dict, comment=comment)


@section_reader('RESERVOIRS', 1)
class ReservoirFactory(ComponentFactory):
    """Factory for parsing and creating Reservoirs and adding them to a Network."""
    def __new__(cls, network: Network, block: dict):
        logger.debug('Reading Reservoirs section')
        for values in block:
            r = cls._parse_single(values, network)
            add_reservoir(network, r)
        logger.debug(f'Added {len(get_reservoirs(network))} Reservoirs')

    @classmethod
    def _parse_single(cls, values, network) -> Reservoir:
        comment = cls._read_comment(values)
        attr_values = cls._pad_list(values['values'], 3)
        attr_names = ['id', 'head', 'headpattern']
        attr_cls = [str, float, Pattern]
        attr_dict = cls._create_attr_dict(attr_names, attr_values, attr_cls, network)
        return Reservoir(**attr_dict, comment=comment)


@section_reader('TANKS', 1)
class TankFactory(ComponentFactory):
    """Factory for parsing and creating Tanks and adding them to a Network."""
    def __new__(cls, network: Network, block: dict):
        logger.debug('Reading Tanks section')
        for values in block:
            t = cls._parse_single(values, network)
            add_tank(network, t)
        logger.debug(f'Added {len(get_tanks(network))} Tanks')

    @classmethod
    def _parse_single(cls, values: dict, network: Network) -> Tank:
        comment = cls._read_comment(values)
        attr_values = cls._pad_list(values['values'], 8)
        attr_names = ['id', 'elevation', 'initlevel', 'minlevel', 'maxlevel', 'diam', 'minvolume', 'volumecurve']
        attr_cls = [str, float, float, float, float, float, float, Curve]
        attr_dict = cls._create_attr_dict(attr_names, attr_values, attr_cls, network)
        return Tank(**attr_dict, comment=comment)


@section_reader('PIPES', 2)
class PipeFactory(ComponentFactory):
    """Factory for parsing and creating Pipes and adding them to a Network."""
    def __new__(cls, network: Network, block: dict):
        logger.debug('Reading Pipes section')
        for values in block:
            p = cls._parse_single(values, network)
            add_pipe(network, p)
        logger.debug(f'Added {len(get_pipes(network))} Pipes')

    @classmethod
    def _parse_single(cls, values: dict, network: Network) -> Pipe:
        comment = cls._read_comment(values)
        attr_values = cls._pad_list(values['values'], 8)
        attr_names = ['id', 'startnode', 'endnode', 'length', 'diameter', 'roughness', 'minorloss', 'status']
        attr_cls = [str, Node, Node, float, float, float, float, str]
        attr_dict = cls._create_attr_dict(attr_names, attr_values, attr_cls, network)
        return Pipe(**attr_dict, comment=comment)


@section_reader('PUMPS', 2)
class PumpFactory(ComponentFactory):
    """Factory for parsing and creating Pumps and adding them to a Network."""
    def __new__(cls, network: Network, block: dict):
        logger.debug('Reading Pumps section')
        for values in block:
            p = cls._parse_single(values, network)
            add_pump(network, p)
        logger.debug(f'Added {len(get_pumps(network))} Pumps')

    @classmethod
    def _parse_single(cls, values: dict, network: Network) -> Pump:
        comment = cls._read_comment(values)
        attr_values = values['values'][:3]
        attr_names = ['id', 'startnode', 'endnode']
        attr_cls = [str, Node, Node]

        prop_names, prop_vals, prop_cls = cls._parse_keywords(values['values'][3:])

        attr_dict = cls._create_attr_dict(attr_names+prop_names, attr_values+prop_vals, attr_cls+prop_cls, network)
        return Pump(**attr_dict, comment=comment)

    @staticmethod
    def _parse_keywords(keywords):
        values = []
        names = []
        cls = []
        for i in range(0, len(keywords), 2):
            try:
                keyword = keywords[i]
                value = keywords[i + 1]
            except IndexError:
                continue
            if keyword in {'POWER', 'SPEED'}:
                names.append(keyword.lower())
                cls.append(float)
            elif keyword == 'HEAD':
                names.append('head')
                cls.append(Curve)
            elif keyword == 'PATTERN':
                names.append('pattern')
                cls.append(Pattern)
            values.append(value)
        return names, values, cls

    @staticmethod
    def _pad_list(alist: list, target_length: int, pump_value_index=4) -> list:
        if len(alist) > pump_value_index:
            pump_values = " ".join(alist[pump_value_index:])
            shortend_list = alist[:pump_value_index]
            shortend_list.append(pump_values)
            alist = shortend_list
        return ComponentFactory._pad_list(alist, target_length)


@section_reader('VALVES', 2)
class ValveFactory(ComponentFactory):
    """Factory for parsing and creating Valves and adding them to a Network."""
    def __new__(cls, network: Network, block: dict):
        logger.debug('Reading Valve section')
        for values in block:
            v = cls._parse_single(values, network)
            add_valve(network, v)
        logger.debug(f'Added {len(get_valves(network))} Valves')

    @classmethod
    def _parse_single(cls, values: dict, network: Network) -> Valve:
        comment = cls._read_comment(values)
        attr_values = values['values']
        valve_type = attr_values[4]
        del attr_values[4]
        attr_values = cls._pad_list(values['values'], 7)
        attr_names = ['id', 'startnode', 'endnode', 'diameter', 'setting', 'minorloss']

        if valve_type in {'PRV', 'TCV', 'PSV', 'PBV', 'FCV'}:
            attr_cls = [str, Node, Node, float, float, float]
        elif valve_type == 'GPV':
            attr_cls = [str, Node, Node, float, Curve, float]
        else:
            raise InvalidValveTypeError(valve_type)
        attr_dict = cls._create_attr_dict(attr_names, attr_values, attr_cls, network)
        return eval(valve_type)(**attr_dict, comment=comment)
