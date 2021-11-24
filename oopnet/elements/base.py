"""
This module contains all the base classes of OOPNET
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class NetworkComponent:
    """
    This is OOPNET's base class for all objects having a name (id) in EPANET Input files
    """

    id: str
    comment: Optional[str] = None
    tag: Optional[str] = None

    def __str__(self):
        return self.id

    def __hash__(self):
        return hash(self.id) + hash(type(self))
