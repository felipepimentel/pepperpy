"""Console types module."""

from dataclasses import dataclass


@dataclass
class ThemeColors:
    """Theme colors configuration."""

    primary: str
    secondary: str
    success: str
    warning: str
    error: str
    info: str
    background: str
    text: str


@dataclass
class Theme:
    """Theme configuration."""

    name: str
    colors: ThemeColors


@dataclass
class LayoutConfig:
    """Layout configuration."""

    width: int
    height: int
    padding: int


@dataclass
class ConsoleConfig:
    """Console configuration."""

    theme: Theme
    layout: LayoutConfig
