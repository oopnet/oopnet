"""
This module contains all the base classes of OOPNET
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from oopnet.elements.network import Network
    

@dataclass
class NetworkComponent(ABC):
    """This is OOPNET's base class for all objects having a name (id) in EPANET Input files

    Attributes:
      id: A unique label used to identify the Network Component. It can consist of a combination of up to 15 numerals or characters. It cannot be the same as the ID for any other node if it is a node, the same counts for links.
      comment: Property containing a comment on the attribute if it is necessary. The comment is automatically read in from EPANET input files by parsing everything behind a semicolon (;), if a semicolon is not the first character in a line
      tag: Associates category labels (tags) with specific nodes and links. An optional text string (with no spaces) used to assign e.g. the node to a category, such as a pressure zone.

    """
    id: str
    _id: str = field(init=False, compare=False, hash=False, repr=False)
    comment: Optional[str] = None
    tag: Optional[str] = None
    _network_: Optional[Network] = field(default=None, init=False, compare=False, hash=False, repr=False)

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    @abstractmethod
    def id(self, value):
        """Abstract method for setting a component's ID"""

    @property
    def _network(self):
        return self._network_

    @_network.setter
    def _network(self, value: Optional[Network]):
        if not self._network_ or value is None:
            self._network_ = value
        else:
            raise RuntimeError('NetworkComponents cannot be added to two different Networks.')

    def _rename(self, id: str, hashtable: dict) -> None:
        if hashtable:
            hashtable[id] = hashtable.pop(self.id)
        self._id = id
