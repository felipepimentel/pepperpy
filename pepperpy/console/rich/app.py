"""Rich application implementation"""

from typing import Any, List, Optional

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.theme import Theme
from rich.traceback import install

from .config import RichConfig
from .exceptions import RichError


class RichApp:
    """Rich console application"""

    def __init__(self, config: Optional[RichConfig] = None):
        self.config = config or RichConfig()
        self.console = Console(
            theme=Theme(self.config.theme),
            record=True,
            force_terminal=self.config.force_terminal,
            force_interactive=self.config.force_interactive,
        )
        self._layout = Layout()
        self._live = None
        install()  # Install rich traceback handler

    async def start(self) -> None:
        """Start rich application"""
        try:
            # Initialize layout
            self._setup_layout()

            # Start live display
            self._live = Live(
                self._layout,
                console=self.console,
                refresh_per_second=self.config.refresh_rate,
                screen=self.config.use_alternate_screen,
            )

            await self._live.__aenter__()

        except Exception as e:
            raise RichError(f"Failed to start application: {str(e)}", cause=e)

    async def stop(self) -> None:
        """Stop rich application"""
        if self._live:
            await self._live.__aexit__(None, None, None)

    def add_panel(
        self, content: Any, title: Optional[str] = None, layout_name: str = "main"
    ) -> None:
        """Add panel to layout"""
        panel = Panel(content, title=title, border_style=self.config.panel_style)
        self._layout[layout_name].update(panel)

    def add_table(
        self,
        columns: List[str],
        rows: List[List[Any]],
        title: Optional[str] = None,
        layout_name: str = "main",
    ) -> None:
        """Add table to layout"""
        table = Table(
            title=title,
            show_header=True,
            header_style=self.config.header_style,
            border_style=self.config.border_style,
        )

        for column in columns:
            table.add_column(column)

        for row in rows:
            table.add_row(*[str(cell) for cell in row])

        self._layout[layout_name].update(table)

    def add_progress(
        self, total: int, description: str = "Processing", layout_name: str = "footer"
    ) -> Progress:
        """Add progress bar"""
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            *self.config.progress_columns,
            console=self.console,
        )

        progress.add_task(description, total=total)
        self._layout[layout_name].update(progress)
        return progress

    def add_markdown(self, content: str, layout_name: str = "main") -> None:
        """Add markdown content"""
        md = Markdown(content, code_theme=self.config.code_theme)
        self._layout[layout_name].update(md)

    def add_code(self, code: str, language: str, layout_name: str = "main") -> None:
        """Add syntax highlighted code"""
        syntax = Syntax(code, language, theme=self.config.code_theme, line_numbers=True)
        self._layout[layout_name].update(syntax)

    def log(self, message: str, style: Optional[str] = None, layout_name: str = "log") -> None:
        """Add log message"""
        self.console.log(message, style=style)
        if layout_name in self._layout:
            current = self._layout[layout_name].renderable
            if hasattr(current, "append"):
                current.append(message)
            else:
                self._layout[layout_name].update(message)

    def clear(self, layout_name: Optional[str] = None) -> None:
        """Clear layout content"""
        if layout_name:
            self._layout[layout_name].update("")
        else:
            for name in self._layout:
                self._layout[name].update("")

    def _setup_layout(self) -> None:
        """Setup default layout"""
        self._layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3),
            Layout(name="log", size=10),
        )
