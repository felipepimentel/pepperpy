"""Panel component"""

from typing import Any, Optional, Union

from rich.box import ROUNDED, Box
from rich.panel import Panel as RichPanel
from rich.style import Style
from rich.text import Text

from .base import Component, ComponentConfig


class Panel(Component):
    """Panel component that wraps content in a border"""

    def __init__(
        self,
        content: Union[str, Component],
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        style: str = "default",
        border_style: Union[str, Box] = ROUNDED,
        padding: tuple = (0, 1),
    ):
        config = ComponentConfig(
            style={
                "title": Style(bold=True),
                "subtitle": Style(dim=True),
                "border": Style(),
            }
        )
        super().__init__(config)
        self.content = content
        self.title = title
        self.subtitle = subtitle
        self.style = style
        self.border_style = border_style if isinstance(border_style, Box) else ROUNDED
        self.padding = padding

    async def initialize(self) -> None:
        """Initialize panel"""
        if isinstance(self.content, Component):
            await self.content.initialize()

    async def cleanup(self) -> None:
        """Cleanup panel"""
        if isinstance(self.content, Component):
            await self.content.cleanup()

    async def handle_input(self, key: Any) -> bool:
        """Handle input event"""
        if isinstance(self.content, Component):
            return await self.content.handle_input(key)
        return False

    def render(self) -> Text:
        """Render panel"""
        content = (
            self.content.render()
            if isinstance(self.content, Component)
            else Text(str(self.content))
        )

        panel = RichPanel(
            content,
            title=f"[bold {self.style}]{self.title}[/]" if self.title else None,
            subtitle=f"[dim]{self.subtitle}[/]" if self.subtitle else None,
            style=self.style,
            box=self.border_style,
            padding=self.padding,
        )

        return Text.from_markup(str(panel))
