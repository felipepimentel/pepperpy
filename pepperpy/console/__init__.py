"""Console module for terminal UI"""

from .base import Console, ConsoleApp, ConsoleConfig
from .legacy import LegacyConsole

__all__ = [
    "Console",
    "ConsoleApp", 
    "ConsoleConfig",
    "LegacyConsole"
]
