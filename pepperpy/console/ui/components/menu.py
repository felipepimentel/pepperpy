"""Menu component"""

from collections.abc import Callable
from dataclasses import dataclass

from .base import Component


@dataclass
class Menu(Component):
    """Menu component"""

    items: list[tuple[str, Callable[[], None]]]
