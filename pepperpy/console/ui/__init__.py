"""Console UI module"""

from .app import ConsoleApp, app
from .components.base import Component, ComponentConfig
from .components.chat import ChatView
from .components.dialog import Dialog
from .components.form import Form, FormField
from .components.layout import Layout
from .components.list import ListView
from .components.panel import Panel
from .components.progress import ProgressBar
from .components.richtext import RichText
from .components.spinner import Spinner
from .components.table import Table
from .components.wizard import Wizard
from .exceptions import InputError, LayoutError, RenderError, UIError
from .keyboard import BACKSPACE, CTRL_C, ENTER, ESCAPE, TAB, Key, KeyboardManager
from .screen import Direction, Screen, ScreenConfig
from .styles import StyleConfig, StyleManager, styles

__all__ = [
    # App
    "ConsoleApp",
    "app",
    # Base
    "Component",
    "ComponentConfig",
    # Components
    "ChatView",
    "Dialog",
    "Form",
    "FormField",
    "Layout",
    "ListView",
    "ProgressBar",
    "RichText",
    "Spinner",
    "Wizard",
    "Panel",
    "Table",
    # Exceptions
    "UIError",
    "InputError",
    "LayoutError",
    "RenderError",
    # Keyboard
    "Key",
    "KeyboardManager",
    "ENTER",
    "ESCAPE",
    "BACKSPACE",
    "TAB",
    "CTRL_C",
    # Screen
    "Screen",
    "ScreenConfig",
    "Direction",
    # Styles
    "StyleConfig",
    "StyleManager",
    "styles",
]
