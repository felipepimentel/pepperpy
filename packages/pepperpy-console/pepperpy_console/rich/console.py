"""Rich console implementation."""

from typing import Any

from rich.console import Console
from rich.style import Style

from ..base.console import BaseConsole, ConsoleConfig


class RichConsole(BaseConsole):
    """Rich console implementation."""

    def __init__(self, config: ConsoleConfig | None = None) -> None:
        """Initialize rich console."""
        super().__init__()
        self.config = config or ConsoleConfig()
        self._console = Console(**self.config.to_kwargs())  # type: ignore

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console."""
        self._console.print(*args, **kwargs)

    def clear(self) -> None:
        """Clear console."""
        self._console.clear()

    def get_width(self) -> int:
        """Get console width."""
        console_width: int = getattr(self._console, "width", 80)
        return console_width

    def get_height(self) -> int:
        """Get console height."""
        console_height: int = getattr(self._console, "height", 24)
        return console_height

    def info(self, message: str) -> None:
        """Print info message."""
        self.print(f"ℹ️ {message}", style=Style(color="blue"))

    def success(self, message: str) -> None:
        """Print success message."""
        self.print(f"✅ {message}", style=Style(color="green"))

    def warning(self, message: str) -> None:
        """Print warning message."""
        self.print(f"⚠️ {message}", style=Style(color="yellow"))

    def error(self, message: str) -> None:
        """Print error message."""
        self.print(f"❌ {message}", style=Style(color="red"))
