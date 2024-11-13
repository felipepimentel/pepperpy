"""Screen management for console UI"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict

from rich.console import Console
from rich.text import Text


class Direction(Enum):
    """Screen scroll direction"""

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class ScreenConfig:
    """Screen configuration"""

    width: int = 80
    height: int = 24
    title: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class Screen:
    """Console screen manager"""

    def __init__(self, config: ScreenConfig | None = None):
        self.config = config or ScreenConfig()
        self._console = Console()

    async def initialize(self) -> None:
        """Initialize screen"""
        self._console.clear()

    async def cleanup(self) -> None:
        """Cleanup screen"""
        self._console.clear()

    def clear(self) -> None:
        """Clear screen"""
        self._console.clear()

    def refresh(self) -> None:
        """Refresh screen"""
        pass

    def print(self, text: Text) -> None:
        """Print text to screen"""
        self._console.print(text)

    def scroll(self, direction: Direction, lines: int = 1) -> None:
        """Scroll screen

        Args:
            direction: Scroll direction
            lines: Number of lines to scroll
        """
        pass
