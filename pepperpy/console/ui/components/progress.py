"""Progress bar component"""

from typing import Any

from rich.style import Style
from rich.text import Text

from .base import Component, ComponentConfig


class ProgressBar(Component):
    """Progress bar component"""

    def __init__(self, total: int = 100) -> None:
        config = ComponentConfig(
            style={
                "bar": Style(color="green"),
                "text": Style(color="white"),
                "percentage": Style(color="cyan"),
            },
            metadata={
                "total": total,
                "show_percentage": True,
                "width": 40,
            },
        )
        super().__init__(config)
        self._total = total
        self._current = 0
        self._description = ""

    async def initialize(self) -> None:
        """Initialize progress bar"""
        self._current = 0
        self._description = ""

    async def cleanup(self) -> None:
        """Cleanup progress bar"""

    async def handle_input(self, key: Any) -> bool:
        """Handle input event"""
        return False

    def set_progress(self, value: int, description: str = "") -> None:
        """Set progress value"""
        self._current = max(0, min(value, self._total))
        self._description = description

    def render(self) -> Text:
        """Render progress bar"""
        width = self.config.metadata.get("width", 40)
        filled = int(width * self._current / self._total)
        empty = width - filled

        bar = Text()

        if self._description:
            bar.append(f"{self._description} ", style=self.config.style.get("text"))

        bar.append("[", style=self.config.style.get("text"))
        bar.append("=" * filled, style=self.config.style.get("bar"))
        bar.append(" " * empty)
        bar.append("]", style=self.config.style.get("text"))

        if self.config.metadata.get("show_percentage", True):
            percentage = (self._current / self._total) * 100
            bar.append(f" {percentage:.1f}%", style=self.config.style.get("percentage"))

        return bar
