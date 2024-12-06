"""Rich console application."""

from rich.console import Console

from .config import RichConfig


class RichApp:
    """Rich console application."""

    def __init__(self, config: RichConfig | None = None) -> None:
        """Initialize rich console application."""
        self.config = config or RichConfig()
        self.console = Console(
            style=self.config.style,
            highlight=self.config.highlight,
            markup=self.config.markup,
            emoji=self.config.emoji,
            color_system=self.config.color_system,
            width=self.config.width,
            height=self.config.height,
            tab_size=self.config.tab_size,
            soft_wrap=self.config.soft_wrap,
        )
