from dataclasses import dataclass
from typing import List

from oopnet.elements.network_components import Node


@dataclass(slots=True)
class Vertex:
    """ """
    # ToDo: Implement Vertex
    """
    .. warning::
        Not implemented yet
    """
    pass


@dataclass(slots=True)
class Label:
    """Assigns coordinates to map labels."""

    xcoordinate: float
    ycoordinate: float
    label: str
    anchor: Node


@dataclass(slots=True)
class Backdrop:
    """Identifies a backdrop image and dimensions for the network map."""

    dimensions: List[float]
    units: str
    file: str
    offset: List[float]


@dataclass(slots=True)
class Tag:
    """Associates category labels (tags) with specific nodes and links."""
    id: str
    comment: str
    object: str  # = Enum('NODE', 'LINK')
    tag: str
