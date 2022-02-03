from dataclasses import dataclass

import numpy as np

from oopnet.elements.network_components import Node


@dataclass
class Vertex:
    xcoordinate: float
    ycoordinate: float

    @property
    def coordinates(self):
        return np.asarray([self.xcoordinate, self.ycoordinate])

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

    dimensions: list[float]
    units: str
    file: str
    offset: list[float]


@dataclass
class Tag:
    """Associates category labels (tags) with specific nodes and links."""
    id: str
    comment: str
    object: str  # = Enum('NODE', 'LINK')
    tag: str
