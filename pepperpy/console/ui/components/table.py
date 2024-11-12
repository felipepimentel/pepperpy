"""Table component"""

from dataclasses import dataclass
from typing import List

from .base import Component


@dataclass
class Table(Component):
    """Table component"""

    columns: List[str]
    data: List[List[str]]
    show_border: bool = True
