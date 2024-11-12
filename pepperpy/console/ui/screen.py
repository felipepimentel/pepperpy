"""Screen management"""

from dataclasses import dataclass
from typing import Optional

from .themes import Theme


@dataclass
class Screen:
    """Screen manager"""

    title: str
    theme: Optional[Theme] = None
    width: Optional[int] = None
    height: Optional[int] = None
