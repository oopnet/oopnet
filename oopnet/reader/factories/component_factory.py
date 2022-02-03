from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from oopnet.elements.base import NetworkComponent
from oopnet.elements.network_components import Node
from oopnet.elements.system_operation import Pattern, Curve
from oopnet.utils.getters.get_by_id import get_pattern, get_curve, get_node
from oopnet.reader.factories.base import ReadFactory
if TYPE_CHECKING:
    from oopnet.elements.network import Network


class ComponentFactory(ReadFactory):
    """Base Factory for creating NetworkComponents and adding them to a Network."""
    @staticmethod
    def _read_comment(values: dict) -> str:
        """Reads comment from values."""
        return values['comments'] or None

    @classmethod
    @abstractmethod
    def _parse_single(cls, values: dict, network: Network) -> NetworkComponent:
        """Abstract method for parsing a single object from values.

        Args:
            values: dictionary representing a row in the EPANET input file
            network: Network to which the NetworkComponent shall be added
        """

    @staticmethod
    def _create_attr_dict(attrs: list[str], values: list[str], cls_list: list, network: Network) -> dict:
        """Creates a dictionary for instantiating a NetworkComponent object.

        Creates a dictionary that can then be unpacked when instantiating a NetworkComponent object. The function casts
        the passed values to the type defined in cls_list. attrs, values and cls_list have to be of the same length to
        work properly.

        Args:
            attrs: list of attribute names of a NetworkComponent object (content depends on exact NetworkComponent type)
            values: list of attribute values to be set
            cls_list: list of attribute types

        Returns:
            dictionary with attribute names as keys and attribute values as values
        """
        attr_dict = {}
        for attr, value, attr_cls in zip(attrs, values, cls_list):
            if value is None:
                continue
            if attr_cls == Pattern:
                value = get_pattern(network, value)
                attr_dict[attr] = value
            elif attr_cls == Curve:
                value = get_curve(network, value)
                attr_dict[attr] = value
            elif attr_cls == Node:
                value = get_node(network, value)
                attr_dict[attr] = value
            elif attr_cls == str and attr != 'id':
                attr_dict[attr] = attr_cls(value.upper())
            else:
                attr_dict[attr] = attr_cls(value)
        return attr_dict
