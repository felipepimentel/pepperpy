"""Console configuration."""

from dataclasses import dataclass
from typing import TextIO


@dataclass
class ConsoleConfig:
    """Console configuration."""

    stderr: bool = False
    file: TextIO | None = None
    force_terminal: bool | None = None
    color_system: str | None = "auto"
    record: bool = False
    markup: bool = True
    emoji: bool = True
    highlight: bool = True
    width: int | None = None
    height: int | None = None
