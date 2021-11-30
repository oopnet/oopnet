"""
This module contains all the base classes of OOPNET
"""
from dataclasses import dataclass
from typing import Optional
from abc import abstractmethod


@dataclass
class NetworkComponent:
    """This is OOPNET's base class for all objects having a name (id) in EPANET Input files

    Attributes:
      id: A unique label used to identify the Network Component. It can consist of a combination of up to 15 numerals or characters. It cannot be the same as the ID for any other node if it is a node, the same counts for links.
      comment: Property containing a comment on the attribute if it is necessary. The comment is automatically read in from EPANET input files by parsing everything behind a semicolon (;), if a semicolon is not the first character in a line
      tag: Associates category labels (tags) with specific nodes and links. An optional text string (with no spaces) used to assign e.g. the node to a category, such as a pressure zone.

    """
    _id: str = ''
    id: str = property(fget=lambda self: self._get_id(),
                       fset=lambda self, value: self._set_id(value))
    comment: Optional[str] = None
    tag: Optional[str] = None
    _network = None

    def __str__(self):
        return self.id

    def __hash__(self):
        return hash(self.id) + hash(type(self))

    def _get_id(self):
        return self._id

    @abstractmethod
    def _set_id(self, id: str):
        """Sets ID of NetworkComponent and replaces key in network hash"""
