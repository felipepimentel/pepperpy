"""UI Themes"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from .default import DEFAULT_THEME


@dataclass
class ThemeColors:
    """Theme color definitions"""

    primary: Tuple[int, int, int]
    secondary: Tuple[int, int, int]
    accent: Tuple[int, int, int]
    background: Tuple[int, int, int]
    foreground: Tuple[int, int, int]


@dataclass
class Theme:
    """UI Theme configuration"""

    name: str
    colors: ThemeColors
    styles: Dict[str, str]
    fonts: Optional[Dict[str, str]] = None


__all__ = ["Theme", "ThemeColors", "DEFAULT_THEME"]
