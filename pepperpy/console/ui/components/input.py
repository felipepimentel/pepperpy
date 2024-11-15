"""Input components"""

from collections.abc import Callable
from dataclasses import dataclass

from .base import Component


@dataclass
class Input(Component):
    """Base input component"""

    placeholder: str = ""
    value: str = ""
    on_change: Callable[[str], None] | None = None


class TextInput(Input):
    """Text input component"""

