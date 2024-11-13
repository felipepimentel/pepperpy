"""Console UI module"""

from .app import ConsoleApp, app
from .components.base import Component, ComponentConfig
from .components.chat import ChatView
from .components.dialog import Dialog
from .components.form import Form, FormField
from .components.list import ListView
from .components.progress import ProgressBar
from .components.richtext import RichText
from .components.spinner import Spinner
from .components.wizard import Wizard
from .exceptions import InputError, LayoutError, RenderError, UIError
from .keyboard import BACKSPACE, CTRL_C, ENTER, ESCAPE, TAB, Key, KeyboardManager
from .layout import Layout
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
    "ListView",
    "ProgressBar",
    "RichText",
    "Spinner",
    "Wizard",
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
    # Layout
    "Layout",
    # Screen
    "Screen",
    "ScreenConfig",
    "Direction",
    # Styles
    "StyleConfig",
    "StyleManager",
    "styles",
]
