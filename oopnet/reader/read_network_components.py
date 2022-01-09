from __future__ import annotations

from abc import abstractmethod

from typing import TYPE_CHECKING

from oopnet.reader.factory_base import ReadFactory, InvalidValveTypeError
from oopnet.elements import Network, Tank, Reservoir, Pipe, Pump, Valve, Node, Pattern, Curve, Junction, FCV, PRV, PBV,\
    PSV, GPV, TCV
from oopnet.utils.getters import get_junction, get_pattern, get_curve, get_node
from oopnet.elements.enums import PipeStatus, PumpStatus, ValveStatus, PumpKeyword, ValveType
from oopnet.utils.adders import *
from oopnet.reader.decorators import section_reader
if TYPE_CHECKING:
    from oopnet.elements import Network


@section_reader('TITLE', 4)
def read_title(network: Network, block: list):
    """Reads the network title from block.

    Args:
      network: OOPNET network object where the title shall be stored
      block: EPANET input file block

    """
    for vals in block:
        vals = vals['values']
        network.title = " ".join(vals)


class ComponentFactory(ReadFactory):
    @staticmethod
    def _read_comment(values: dict) -> str:
        return values['comments'] or None

    @classmethod
    @abstractmethod
    def _parse_single(cls, values, network):
        pass

    @staticmethod
    def _create_attr_dict(attrs: list[str], values: list[str], cls_list: list, network: Network) -> dict:
        attr_dict = {}
        for attr, value, attr_cls in zip(attrs, values, cls_list):
            if attr_cls == Pattern:
                value = get_pattern(network, value) if value else None
                attr_dict[attr] = value
            elif attr_cls == Curve:
                value = get_curve(network, value) if value else None
                attr_dict[attr] = value
            elif attr_cls == Node:
                value = get_node(network, value)
                attr_dict[attr] = value
            elif attr_cls in {PipeStatus, PumpStatus, ValveStatus, PumpKeyword}:
                attr_dict[attr] = attr_cls(value.upper())
            elif value is not None:
                attr_dict[attr] = attr_cls(value)
        return attr_dict


@section_reader('EMITTERS', 4)
class EmitterFactory(ComponentFactory):
    def __new__(cls, network: Network, block: dict):
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


@section_reader('EMITTERS', 2)
def read_emitters(network: Network, block: list):
    """Reads emitters from block.

    Args:
      network: OOPNET network object where the emitters shall be stored
      block: EPANET input file block

    """
    for vals in block:
        vals = vals['values']
        j = get_junction(network, vals[0])
        j.emittercoefficient = float(vals[1])


@section_reader('JUNCTIONS', 1)
class JunctionFactory(ComponentFactory):
    def __new__(cls, network: Network, block: dict):
        for values in block:
            j = cls._parse_single(values, network)
            add_junction(network, j, False)

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
    def __new__(cls, network: Network, block: dict):
        for values in block:
            r = cls._parse_single(values, network)
            add_reservoir(network, r, False)

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
    def __new__(cls, network: Network, block: dict):
        for values in block:
            t = cls._parse_single(values, network)
            add_tank(network, t, False)

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
    def __new__(cls, network: Network, block: dict):
        for values in block:
            p = cls._parse_single(values, network)
            add_pipe(network, p, False)

    @classmethod
    def _parse_single(cls, values: dict, network: Network) -> Pipe:
        comment = cls._read_comment(values)
        attr_values = cls._pad_list(values['values'], 8)
        attr_names = ['id', 'startnode', 'endnode', 'length', 'diameter', 'roughness', 'minorloss', 'status']
        attr_cls = [str, Node, Node, float, float, float, float, PipeStatus]
        attr_dict = cls._create_attr_dict(attr_names, attr_values, attr_cls, network)
        return Pipe(**attr_dict, comment=comment)


@section_reader('PUMPS', 2)
class PumpFactory(ComponentFactory):
    def __new__(cls, network: Network, block: dict):
        for values in block:
            p = cls._parse_single(values, network)
            add_pump(network, p, False)

    @classmethod
    def _parse_single(cls, values: dict, network: Network) -> Pump:
        comment = cls._read_comment(values)
        attr_values = cls._pad_list(values['values'], 5)
        attr_names = ['id', 'startnode', 'endnode', 'keyword', 'value']
        attr_cls = [str, Node, Node, PumpKeyword, str]
        attr_dict = cls._create_attr_dict(attr_names, attr_values, attr_cls, network)
        return Pump(**attr_dict, comment=comment)

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
    def __new__(cls, network: Network, block: dict):
        for values in block:
            v = cls._parse_single(values, network)
            add_valve(network, v, False)

    @classmethod
    def _parse_single(cls, values: dict, network: Network) -> Valve:
        comment = cls._read_comment(values)
        attr_values = values['values']
        valve_type = attr_values[4]
        attr_values = cls._pad_list(values['values'], 7)
        attr_names = ['id', 'startnode', 'endnode', 'diameter', 'valvetype', 'setting', 'minorloss']

        if valve_type in {'PRV', 'TCV', 'PSV', 'PBV', 'FCV'}:
            attr_cls = [str, Node, Node, float, ValveType, float, float]
        elif valve_type == 'GPV':
            # todo: switch GPV values to Curves
            attr_cls = [str, Node, Node, float, ValveType, str, float]
        else:
            raise InvalidValveTypeError(valve_type)
        attr_dict = cls._create_attr_dict(attr_names, attr_values, attr_cls, network)
        return eval(valve_type)(**attr_dict, comment=comment)
