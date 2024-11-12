"""Button component"""

from dataclasses import dataclass
from typing import Callable, Optional

from .base import Component


@dataclass
class Button(Component):
    """Button component"""

    text: str
    on_click: Optional[Callable[[], None]] = None
