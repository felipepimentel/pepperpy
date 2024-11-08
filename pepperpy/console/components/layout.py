from typing import List, Optional, Union

from rich.console import Console
from rich.layout import Layout as RichLayout
from rich.panel import Panel
from rich.text import Text


class Layout:
    """Console layout manager for organized output"""

    def __init__(self, console: Console):
        self._console = console
        self._layout = RichLayout()

    def split(self, direction: str = "vertical", names: Optional[List[str]] = None) -> None:
        """Split layout into sections"""
        self._layout.split(direction, *names if names else [])

    def add_panel(
        self, content: Union[str, Text], title: Optional[str] = None, section: Optional[str] = None
    ) -> None:
        """Add panel to layout section"""
        panel = Panel(content, title=title)
        if section:
            self._layout[section].update(panel)
        else:
            self._layout.update(panel)

    def show(self) -> None:
        """Display current layout"""
        self._console.print(self._layout)
