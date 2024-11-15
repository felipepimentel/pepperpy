"""Button component"""

from collections.abc import Callable
from dataclasses import dataclass

from .base import Component


@dataclass
class Button(Component):
    """Button component"""

    text: str
    on_click: Callable[[], None] | None = None
