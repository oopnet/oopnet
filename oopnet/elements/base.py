"""
This module contains all the base classes of OOPNET
"""
from dataclasses import dataclass, field
from typing import Optional

from oopnet.exceptions import ComponentExistsError


@dataclass
class NetworkComponent:
    """This is OOPNET's base class for all objects having a name (id) in EPANET Input files

    Attributes:
      id: A unique label used to identify the Network Component. It can consist of a combination of up to 15 numerals or characters. It cannot be the same as the ID for any other node if it is a node, the same counts for links.
      comment: Property containing a comment on the attribute if it is necessary. The comment is automatically read in from EPANET input files by parsing everything behind a semicolon (;), if a semicolon is not the first character in a line
      tag: Associates category labels (tags) with specific nodes and links. An optional text string (with no spaces) used to assign e.g. the node to a category, such as a pressure zone.

    """
    id: str
    _id: str = field(init=False, repr=False)
    comment: Optional[str] = None
    tag: Optional[str] = None
    _component_hash: dict = field(default=None, init=False, compare=False, hash=False, repr=False)

    def __hash__(self):
        return hash(self.id) + hash(type(self))

    # def __getstate__(self):
    #     # Copy the object's state from self.__dict__ which contains
    #     # all our instance attributes. Always use the dict.copy()
    #     # method to avoid modifying the original state.
    #     state = self.__dict__.copy()
    #     # Remove the unpicklable entries.
    #     del state['_component_hash']
    #     return state

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets ID of NetworkComponent and replaces key in network hash"""
        if self._component_hash:
            if id in self._component_hash:
                raise ComponentExistsError(id)
            self._component_hash[id] = self
            del self._component_hash[self._id]
        self._id = id
