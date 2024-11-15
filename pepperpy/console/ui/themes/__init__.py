"""UI Themes"""

from dataclasses import dataclass

from .default import DEFAULT_THEME


@dataclass
class ThemeColors:
    """Theme color definitions"""

    primary: tuple[int, int, int]
    secondary: tuple[int, int, int]
    accent: tuple[int, int, int]
    background: tuple[int, int, int]
    foreground: tuple[int, int, int]


@dataclass
class Theme:
    """UI Theme configuration"""

    name: str
    colors: ThemeColors
    styles: dict[str, str]
    fonts: dict[str, str] | None = None


__all__ = ["Theme", "ThemeColors", "DEFAULT_THEME"]
