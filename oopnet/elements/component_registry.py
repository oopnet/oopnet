from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from oopnet.elements.base import NetworkComponent


@dataclass
class ComponentRegistry(dict):
    """Class for storing NetworkComponents in a Network object or a SuperComponentRegistry.

    Based on built-in dict but prevents overwriting an existing key and raises a ComponentNotExistingError error,
    when trying to look up a not exiting Component (instead of default KeyErrors).

    """
    super_registry: Optional[SuperComponentRegistry] = field(default=None, compare=False, hash=False,
                                                             repr=False)

    def __setitem__(self, key, value: NetworkComponent):
        if self.super_registry and self.super_registry.check_id_exists(key):
            raise ComponentExistsError(key)
        elif not self.super_registry and key in self:
            raise ComponentExistsError(key)
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

    def __getitem__(self, item) -> Union[NetworkComponent, ComponentRegistry]:
        """Getter method.

        If item is a key in SuperComponentRegistry, the method returns the corresponding ComponentRegistry. If not,
        it looks for the key in the individual ComponentRegistries themselves.

        Raises:
            ComponentNotExistingError is raised, if the item is not found.

        Returns:
            Either a ComponentRegistry or a NetworkComponent is returned.

        """
        if item in self:
            return super().__getitem__(item)

        for values in self.values():
            if item in values:
                return values[item]
        raise ComponentNotExistingError(item)

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
        return SuperComponentRegistry(['junctions', 'tanks', 'reservoirs'])


class LinkRegistry:
    """SuperComponentRegistry factory for Link components."""
    def __new__(cls, *args, **kwargs):
        return SuperComponentRegistry(['pipes', 'pumps', 'valves'])


class ComponentExistsError(Exception):
    """Raised when a component with the same ID already exists in the network."""
    def __init__(self, id, message=None):
        if not message:
            self.message = f'A conflicting component with the ID "{id}" already exists in the network.'
        super().__init__(self.message)


class ComponentNotExistingError(Exception):
    """Raised when a no component with the ID exists in the network."""
    def __init__(self, id, message=None):
        if not message:
            self.message = f'No Component with ID "{id}" found in the network.'
        super().__init__(self.message)
