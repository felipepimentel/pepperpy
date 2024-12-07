"""Legacy console implementation."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from rich.console import Console as ConsoleType
else:
    from rich._console import Console as ConsoleType

from rich.markup import escape
from rich.panel import Panel
from rich.text import Text

from .base.console import BaseConsole, ConsoleConfig
from .rich.types import RichConsoleProtocol


class LegacyConsole(BaseConsole):
    """Legacy console implementation."""

    _console: RichConsoleProtocol

    def __init__(self, config: ConsoleConfig | None = None) -> None:
        """Initialize legacy console."""
        super().__init__()
        self.config = config or ConsoleConfig()
        self._console = ConsoleType(**self.config.to_kwargs())  # type: ignore

    def clear(self) -> None:
        """Clear console screen."""
        self._console.clear()

    def print(self, content: Any) -> None:  # type: ignore
        """Print content to console."""
        if hasattr(content, "render"):
            # Handle async rendering in a sync context
            rendered_content = content.render()  # type: ignore
            self._console.print(rendered_content)
        else:
            self._console.print(content)

    def success(
        self, message: str, *, title: str | None = None, content: str | None = None
    ) -> None:
        """Print success message with optional title and content."""
        if title or content:
            text = Text()
            if title:
                text.append(f"{title}\n", style="bold green")
            if content:
                text.append(escape(str(content)))
            self._console.print(Panel(text, style="green"))
        else:
            self._console.print(f"✅ {escape(message)}", style="green bold")

    def error(self, *messages: str) -> None:
        """Print error message"""
        message = " ".join(str(m) for m in messages)
        self._console.print(f"❌ {escape(message)}", style="red bold")

    def warning(self, message: str) -> None:
        """Print warning message"""
        self._console.print(f"⚠️ {escape(message)}", style="yellow bold")

    def info(
        self, message: str, *, title: str | None = None, subtitle: str | None = None
    ) -> None:
        """Print info message with optional title and subtitle"""
        if title or subtitle:
            text = Text()
            if title:
                text.append(f"{title}\n", style="bold blue")
            if subtitle:
                text.append(f"{subtitle}\n", style="blue")
            text.append(escape(message))
            self._console.print(Panel(text, style="blue"))
        else:
            self._console.print(f"ℹ️ {escape(message)}", style="blue bold")

    def print_message(
        self, message: str, style: str | None = None, markup: bool | None = None
    ) -> None:
        """Print message."""

    def format_text(
        self, text: str, style: str | None = None, markup: bool | None = None
    ) -> str:
        """Format text."""
        return text

    def setup_legacy_console(self) -> None:
        """Setup legacy console configuration."""
        # ...
