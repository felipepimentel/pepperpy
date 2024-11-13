"""Progress bar component for console UI"""

from typing import Any, Optional

from rich.progress import Progress as RichProgress
from rich.style import Style
from rich.text import Text

from pepperpy.console.ui.components.base import Component, ComponentConfig


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
        super().__init__(config=config)
        self._progress = RichProgress()
        self._task_id: Optional[int] = None
        self._total = total
        self._current = 0
        self._description = ""

    def set_progress(self, value: int, description: str = "") -> None:
        """Set progress value

        Args:
            value: Progress value (0-100)
            description: Progress description
        """
        self._current = max(0, min(value, self._total))
        self._description = description

    def increment(self, amount: int = 1) -> None:
        """Increment progress by amount

        Args:
            amount: Amount to increment
        """
        self.set_progress(self._current + amount)

    def render(self) -> Text:
        """Render progress bar

        Returns:
            Text: Rendered progress bar
        """
        width = self.config.metadata.get("width", 40)
        filled = int(width * self._current / self._total)
        empty = width - filled

        # Criar o texto da barra de progresso
        bar = Text()

        # Adicionar descrição
        if self._description:
            bar.append(f"{self._description} ", style=self.config.style.get("text"))

        # Adicionar a barra
        bar.append("[", style=self.config.style.get("text"))
        bar.append("=" * filled, style=self.config.style.get("bar"))
        bar.append(" " * empty)
        bar.append("]", style=self.config.style.get("text"))

        # Adicionar a porcentagem
        if self.config.metadata.get("show_percentage", True):
            percentage = (self._current / self._total) * 100
            bar.append(f" {percentage:.1f}%", style=self.config.style.get("percentage"))

        return bar

    def __enter__(self) -> "ProgressBar":
        """Enter context manager"""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager"""
        pass
