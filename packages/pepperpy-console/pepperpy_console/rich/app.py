"""Rich console application module."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from rich.console import Console
else:
    from rich._console import Console

from ..base.app import BaseApp
from ..base.console import ConsoleConfig
from ..rich.types import RichConsoleProtocol


class RichApp(BaseApp):
    """Rich console application."""

    _console: RichConsoleProtocol

    def __init__(self, config: ConsoleConfig | None = None) -> None:
        """Initialize rich app."""
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
