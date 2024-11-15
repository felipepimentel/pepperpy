"""Console module for terminal UI and interactions"""

from .base import Console, ConsoleConfig
from .rich import RichConsoleApp
from .ui import UIApp, UIConfig

__all__ = [
    # Base
    "Console",
    "ConsoleConfig",
    # Rich
    "RichConsoleApp",
    # UI
    "UIApp",
    "UIConfig"
]
