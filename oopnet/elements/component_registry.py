from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from oopnet.elements.base import NetworkComponent


class ComponentRegistry(dict):
    """Class for storing NetworkComponents in a Network object or a SuperComponentRegistry.

    Based on built-in dict but prevents overwriting an existing key and raises a ComponentNotExistingError error,
    when trying to look up a not exiting Component (instead of default KeyErrors).

    """

    def __init__(self, super_registry: Optional[SuperComponentRegistry] = None):
        super().__init__()
        self.super_registry = super_registry

    def __setitem__(self, key, value: NetworkComponent):
        if (
            key in self
            or self.super_registry
            and self.super_registry.check_id_exists(key)
        ):
            raise IdenticalIDError(key)
        else:
            super().__setitem__(key, value)

    def __getitem__(self, item) -> NetworkComponent:
        if item not in self:
            raise ComponentNotExistingError(item)
        else:
            return super().__getitem__(item)


class SuperComponentRegistry(dict):
    """Registry for Link and Node components.

    Components are stored in ComponentRegistries for the individual subclasses (junctions, pipes, tanks, ...).

    """

    def __init__(self, classes: list):
        """SuperComponentRegistry init method.

        Args:
            classes: list of class names to be used as keys (e.g., ["junctions", "tanks", "reservoirs"]

        """
        super().__init__()
        for cls in classes:
            self[cls] = ComponentRegistry(super_registry=self)

    def check_id_exists(self, id) -> bool:
        """Checks if a component with the specified ID already exists in one of the ComponentRegistries.

        Args:
            id: ID to check

        Returns:
            True, if the ID exists, False otherwise.

        """
        return any(id in x for x in self.values())


class NodeRegistry:
    """SuperComponentRegistry factory for Node components."""

    def __new__(cls, *args, **kwargs):
        return SuperComponentRegistry(["junctions", "tanks", "reservoirs"])


class LinkRegistry:
    """SuperComponentRegistry factory for Link components."""

    def __new__(cls, *args, **kwargs):
        return SuperComponentRegistry(["pipes", "pumps", "valves"])


class IdenticalIDError(Exception):
    """Raised when a component with the same ID already exists in the network."""

    def __init__(self, id, message=None):
        if not message:
            self.message = f"A conflicting component with the ID {id} already exists in the network."
        super().__init__(self.message)


class ComponentNotExistingError(Exception):
    """Raised when a no component with the ID exists in the network."""

    def __init__(self, id, message=None):
        if not message:
            self.message = f"No Component with ID {id} found in the network."
        super().__init__(self.message)
