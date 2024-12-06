"""Rich console implementation."""

from dataclasses import dataclass, field
from typing import Any, Literal, TextIO

from rich.console import Console as RichConsole

from ..base.console import BaseConsole

# Define valid color system types
ColorSystem = Literal["auto", "standard", "256", "truecolor", "windows"]


@dataclass
class ConsoleConfig:
    """Console configuration."""

    style: str = "default"
    width: int | None = None
    height: int | None = None
    color_system: ColorSystem = "auto"
    stderr: bool = False
    file: TextIO | None = None
    quiet: bool = False
    markup: bool = True
    emoji: bool = True
    highlight: bool = True
    record: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class Console(BaseConsole):
    """Rich console implementation."""

    def __init__(self, config: ConsoleConfig | None = None) -> None:
        """Initialize console."""
        super().__init__()
        self.config = config or ConsoleConfig()
        self._console = RichConsole(
            stderr=self.config.stderr,
            file=self.config.file,
            color_system=self.config.color_system,
            record=self.config.record,
            markup=self.config.markup,
            emoji=self.config.emoji,
            highlight=self.config.highlight,
            width=self.config.width,
            height=self.config.height,
        )

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console."""
        style = kwargs.pop("style", self.config.style)
        self._console.print(*args, style=style, **kwargs)

    def clear(self) -> None:
        """Clear console."""
        self._console.clear()

    def get_width(self) -> int:
        """Get console width."""
        return self._console.width or 80

    def get_height(self) -> int:
        """Get console height."""
        return self._console.height or 24
