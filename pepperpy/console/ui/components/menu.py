"""Menu component"""

from dataclasses import dataclass
from typing import Callable, List, Tuple

from .base import Component


@dataclass
class Menu(Component):
    """Menu component"""

    items: List[Tuple[str, Callable[[], None]]]
