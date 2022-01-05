from __future__ import annotations
from dataclasses import dataclass
from typing import List

from oopnet.elements.enums import TagObject
from oopnet.elements.network_components import Node


@dataclass
class Vertex:
    """ """
    # ToDo: Implement Vertex
    """
    .. warning::
        Not implemented yet
    """
    pass


@dataclass
class Label:
    """Assigns coordinates to map labels."""

    xcoordinate: float
    ycoordinate: float
    label: str
    anchor: Node


@dataclass
class Backdrop:
    """Identifies a backdrop image and dimensions for the network map."""

    dimensions: List[float]
    units: str
    file: str
    offset: List[float]


@dataclass
class Tag:
    """Associates category labels (tags) with specific nodes and links."""
    id: str
    comment: str
    object: TagObject  # = Enum('NODE', 'LINK')
    tag: str
