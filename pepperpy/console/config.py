"""Console configuration"""

from dataclasses import dataclass, field
from enum import Enum

from pepperpy.core.types import JsonDict, ModuleConfig


class ConsoleMode(str, Enum):
    """Console mode"""

    BASIC = "basic"
    RICH = "rich"
    INTERACTIVE = "interactive"
    LEGACY = "legacy"


class ConsoleTheme(str, Enum):
    """Console theme"""

    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"
    CUSTOM = "custom"


@dataclass
class ConsoleConfig(ModuleConfig):
    """Console configuration"""

    name: str
    mode: ConsoleMode = ConsoleMode.RICH
    theme: ConsoleTheme = ConsoleTheme.DEFAULT
    enabled: bool = True
    show_timestamps: bool = True
    show_levels: bool = True
    show_colors: bool = True
    width: int | None = None
    height: int | None = None
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class ConsoleUIConfig(ModuleConfig):
    """Console UI configuration"""

    name: str
    enabled: bool = True
    show_header: bool = True
    show_footer: bool = True
    show_progress: bool = True
    show_status: bool = True
    refresh_rate: float = 0.1  # seconds
    metadata: JsonDict = field(default_factory=dict)
