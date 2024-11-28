"""Console module for PepperPy framework"""

from .base import Console, ConsoleConfig
from .components import (
    Button,
    ButtonConfig,
    ChatView,
    Dialog,
    Form,
    Input,
    Layout,
    ListView,
    Menu,
    Panel,
    PanelConfig,
    ProgressBar,
    Table,
    Toast,
)
from .styles import Style

__version__ = "0.1.0"

__all__ = [
    "Console",
    "ConsoleConfig",
    # Components
    "Button",
    "ButtonConfig",
    "ChatView",
    "Dialog",
    "Form",
    "Input",
    "Layout",
    "ListView",
    "Menu",
    "Panel",
    "PanelConfig",
    "ProgressBar",
    "Table",
    "Toast",
    # Styles
    "Style",
]
