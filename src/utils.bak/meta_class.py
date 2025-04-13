"""Meta Classes.

Module for meta classes.
"""

from typing import Any


class ImmutableMeta(type):
    """Meta Class: Immutable class variables.

    This metaclass makes class variables immutable.
    """
    def __setattr__(cls, name: str, value: Any) -> None:
        """Meta Class with immutable class variables.

        Meta Class to make class variables immutable.

        Args:
            name (str): The name of the attribute to be set.
            value (Any): The value to be assigned to the attribute.

        Raises:
            AttributeError: If the class variable is already set.
        """
        if name in cls.__dict__:
            raise AttributeError(
                f"Cannot modify immutable class variable: '{name}'"
            )
        super().__setattr__(name=name, value=value)
