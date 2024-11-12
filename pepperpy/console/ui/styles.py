"""UI styling definitions"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Color:
    """ANSI color definition"""

    r: int
    g: int
    b: int

    def __str__(self) -> str:
        return f"\033[38;2;{self.r};{self.g};{self.b}m"


@dataclass
class Style:
    """Component style definition"""

    fg_color: Optional[Color] = None
    bg_color: Optional[Color] = None
    bold: bool = False
    italic: bool = False
    underline: bool = False

    def apply(self) -> str:
        """Get ANSI escape sequence for style"""
        style = ""
        if self.fg_color:
            style += str(self.fg_color)
        if self.bg_color:
            style += f"\033[48;2;{self.bg_color.r};{self.bg_color.g};{self.bg_color.b}m"
        if self.bold:
            style += "\033[1m"
        if self.italic:
            style += "\033[3m"
        if self.underline:
            style += "\033[4m"
        return style

    def reset(self) -> str:
        """Reset all styles"""
        return "\033[0m"


@dataclass
class Theme:
    """UI theme definition"""

    primary: Style
    secondary: Style
    accent: Style
    error: Style
    success: Style
    warning: Style
    info: Style
    disabled: Style
