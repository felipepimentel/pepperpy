"""Style definitions for console components"""

from dataclasses import dataclass
from typing import Any, Literal

ColorType = Literal["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
StyleType = Literal["bold", "dim", "italic", "underline", "blink", "reverse", "hidden"]


@dataclass
class Style:
    """Component style configuration"""

    color: ColorType | None = None
    background: ColorType | None = None
    styles: list[StyleType] | None = None

    def __str__(self) -> str:
        """Convert style to string"""
        parts = []

        if self.color:
            parts.append(self.color)

        if self.background:
            parts.append(f"on_{self.background}")

        if self.styles:
            parts.extend(self.styles)

        return " ".join(parts)

    def to_rich_style(self) -> Any:
        """Convert to rich style object"""
        from rich.style import Style as RichStyle

        return RichStyle(**self.__dict__)
