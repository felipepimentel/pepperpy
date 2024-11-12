"""Console module for terminal UI"""

from typing import Dict

from .core.app import ConsoleApp
from .core.config import ConsoleConfig
from .rich.app import RichConsole
from .ui.components import (
    Button,
    Input,
    Menu,
    Table,
    TextInput,
    Toast,
    ToastType,
)
from .ui.components.wizard import WizardStep
from .ui.layout import Layout
from .ui.screen import Screen
from .ui.styles import Style
from .ui.themes import Theme

# Aliases for backward compatibility
Console = RichConsole


# Templates singleton
class ConsoleTemplates:
    """Console template manager"""

    _templates: Dict[str, str] = {}

    @classmethod
    def add(cls, name: str, template: str) -> None:
        """Add template"""
        cls._templates[name] = template

    @classmethod
    def get(cls, name: str) -> str:
        """Get template"""
        return cls._templates.get(name, "")


__all__ = [
    "Console",
    "ConsoleApp",
    "ConsoleConfig",
    "ConsoleTemplates",
    "Screen",
    "Style",
    "Theme",
    "Button",
    "Input",
    "TextInput",
    "Menu",
    "Table",
    "Toast",
    "ToastType",
    "Layout",
    "WizardStep",
]
