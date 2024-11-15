"""Console module for terminal UI"""

from typing import Any

from rich.console import Console as RichConsole
from rich.panel import Panel

from .core.app import ConsoleApp
from .core.config import ConsoleConfig
from .ui.components.button import Button
from .ui.components.input import Input, TextInput
from .ui.components.layout import Layout
from .ui.components.menu import Menu
from .ui.components.table import Table
from .ui.components.toast import Toast, ToastType
from .ui.components.wizard import WizardStep
from .ui.screen import Screen
from .ui.styles import Style
from .ui.themes import Theme


class Console:
    """Simplified console interface wrapping Rich functionality"""

    def __init__(self):
        self._console = RichConsole()

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console"""
        self._console.print(*args, **kwargs)

    def clear(self) -> None:
        """Clear console"""
        self._console.clear()

    def success(
        self,
        content: str,
        title: str | None = None,
        subtitle: str | None = None,
    ) -> None:
        """Display success message in a green panel"""
        self._print_panel(content, title, subtitle, "green")

    def error(self, message: str, error: Any = None) -> None:
        """Display error message in a red panel"""
        content = f"{message}\n{error!s}" if error else message
        if hasattr(error, "cause") and error.cause:
            content += f"\nCause: {error.cause!s}"
        self._print_panel(content, "Error", border_style="red")

    def info(self, message: str) -> None:
        """Display info message in a yellow panel"""
        self._print_panel(message, border_style="yellow")

    def warning(self, message: str) -> None:
        """Display warning message"""
        self.print(f"⚠️  {message}", style="yellow")

    def _print_panel(
        self,
        content: str,
        title: str | None = None,
        subtitle: str | None = None,
        border_style: str = "cyan",
    ) -> None:
        """Internal method to print styled panel"""
        self._console.print(
            Panel(
                content,
                title=f"[bold]{title}[/]" if title else None,
                subtitle=subtitle,
                border_style=border_style,
            ),
        )


# Templates singleton
class ConsoleTemplates:
    """Console template manager"""

    _templates: dict[str, str] = {}

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
