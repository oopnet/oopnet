from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from oopnet.elements.base import NetworkComponent
    from oopnet.elements.network_components import Node


@dataclass
class Vertex:
    """Vertex class.

    Attributes:
          xcoordinate: Vertex xcoordinate
          ycoordinate: Vertex ycoordinate

    """
    xcoordinate: float
    ycoordinate: float

    @property
    def coordinates(self):
        """Vertex x- and y-coordinate."""
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
    object: NetworkComponent
    tag: str
