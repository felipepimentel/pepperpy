"""Console module configuration"""

from dataclasses import dataclass
from typing import Any

from pepperpy.core.config import ModuleConfig


@dataclass
class ConsoleConfig(ModuleConfig):
    """Console configuration"""
    name: str = "console"
    version: str = "1.0.0"
    style: str = "default"
    color_system: str = "auto"
    highlight: bool = True
    markup: bool = True
    emoji: bool = True
    width: int | None = None
    height: int | None = None
    tab_size: int = 4
    soft_wrap: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "style": self.style,
            "color_system": self.color_system,
            "highlight": self.highlight,
            "markup": self.markup,
            "emoji": self.emoji,
            "width": self.width,
            "height": self.height,
            "tab_size": self.tab_size,
            "soft_wrap": self.soft_wrap,
        } 