"""Input components"""

from dataclasses import dataclass
from typing import Callable, Optional

from .base import Component


@dataclass
class Input(Component):
    """Base input component"""

    placeholder: str = ""
    value: str = ""
    on_change: Optional[Callable[[str], None]] = None


class TextInput(Input):
    """Text input component"""

    pass
