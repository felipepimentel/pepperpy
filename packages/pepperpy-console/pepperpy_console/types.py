"""Console types."""

from dataclasses import dataclass, field
from typing import Any, TypedDict

JsonDict = dict[str, Any]


class ThemeColors(TypedDict):
    """Theme colors."""

    primary: str
    secondary: str
    accent: str
    background: str
    foreground: str


@dataclass
class Theme:
    """Console theme."""

    name: str
    colors: ThemeColors
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class LayoutConfig:
    """Layout configuration."""

    width: int
    height: int
    padding: int = 1
    margin: int = 0
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class ConsoleConfig:
    """Console configuration."""

    theme: Theme
    layout: LayoutConfig
    debug: bool = False
    metadata: JsonDict = field(default_factory=dict)
