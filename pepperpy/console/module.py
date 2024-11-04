from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, List, Optional

from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.status import Status
from rich.style import Style
from rich.table import Table
from rich.theme import Theme
from textual.app import App

from pepperpy.core import BaseModule


@dataclass
class ConsoleConfig:
    """Configuration for console module"""

    theme: Dict[str, str] = field(
        default_factory=lambda: {
            "info": "cyan",
            "warning": "yellow",
            "error": "red bold",
            "success": "green",
            "heading": "blue bold",
            "prompt": "magenta",
            "table.header": "blue bold",
            "table.row": "white",
            "panel.border": "blue",
        }
    )
    width: Optional[int] = None
    height: Optional[int] = None
    enable_rich: bool = True
    enable_tui: bool = True
    enable_cli: bool = True
    show_timestamps: bool = True


class ConsoleModule(BaseModule):
    """Enhanced console capabilities"""

    __module_name__ = "console"
    __version__ = "0.1.0"
    __description__ = "Rich console, TUI and CLI capabilities"

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self._console: Optional[RichConsole] = None
        self._theme: Optional[Theme] = None
        self._tui_app: Optional[App] = None

    async def initialize(self) -> None:
        """Initialize console components"""
        await super().initialize()

        # Setup rich console
        if self.config.settings.get("enable_rich", True):
            theme = Theme(
                {
                    k: Style.parse(v)
                    for k, v in self.config.settings.get("theme", {}).items()
                }
            )
            self._console = RichConsole(
                theme=theme,
                width=self.config.settings.get("width"),
                height=self.config.settings.get("height"),
            )

    def print(self, *args, style: Optional[str] = None, **kwargs) -> None:
        """Print with rich formatting"""
        if self._console:
            self._console.print(*args, style=style, **kwargs)
        else:
            print(*args, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Print info message"""
        self.print(f"ℹ️ {message}", style="info", **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Print warning message"""
        self.print(f"⚠️ {message}", style="warning", **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Print error message"""
        self.print(f"❌ {message}", style="error", **kwargs)

    def success(self, message: str, **kwargs) -> None:
        """Print success message"""
        self.print(f"✅ {message}", style="success", **kwargs)

    def heading(self, message: str, **kwargs) -> None:
        """Print heading"""
        self.print(f"\n=== {message} ===\n", style="heading", **kwargs)

    async def prompt(
        self,
        message: str,
        choices: Optional[List[str]] = None,
        default: Optional[str] = None,
        password: bool = False,
        **kwargs,
    ) -> str:
        """Get user input with validation"""
        if password:
            return Prompt.ask(
                message,
                password=True,
                style="prompt",
                console=self._console,
                default=default,
                **kwargs,
            )

        if choices:
            return Prompt.ask(
                message,
                choices=choices,
                style="prompt",
                console=self._console,
                default=default,
                show_choices=True,
                **kwargs,
            )

        return Prompt.ask(
            message, style="prompt", console=self._console, default=default, **kwargs
        )

    def create_table(
        self, title: Optional[str] = None, headers: Optional[List[str]] = None
    ) -> Table:
        """Create rich table"""
        table = Table(
            title=title,
            show_header=bool(headers),
            header_style="table.header",
            row_styles=["table.row"],
        )

        if headers:
            for header in headers:
                table.add_column(header)

        return table

    def create_panel(
        self, content: Any, title: Optional[str] = None, **kwargs
    ) -> Panel:
        """Create rich panel"""
        return Panel(content, title=title, border_style="panel.border", **kwargs)

    @contextmanager
    def progress(
        self, description: str = "Processing", total: Optional[int] = None
    ) -> Generator[Progress, None, None]:
        """Show progress indicator"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self._console,
        ) as progress:
            task_id = progress.add_task(description, total=total)
            yield progress
            progress.update(task_id, completed=True)

    @contextmanager
    def status(self, message: str) -> Generator[Status, None, None]:
        """Show status spinner"""
        with self._console.status(message) as status:
            yield status
