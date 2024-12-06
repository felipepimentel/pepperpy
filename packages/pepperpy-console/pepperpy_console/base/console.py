"""Base console module."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal, TextIO

from rich.console import Console as RichConsole
from rich.style import Style

# Define valid color system types
ColorSystem = Literal["auto", "standard", "256", "truecolor", "windows"]


@dataclass
class ConsoleConfig:
    """Console configuration."""

    stderr: bool = False
    file: TextIO | None = None
    force_terminal: bool | None = None
    color_system: ColorSystem | None = "auto"
    record: bool = False
    markup: bool = True
    emoji: bool = True
    highlight: bool = True
    width: int | None = None
    height: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseConsole(ABC):
    """Base console interface."""

    @abstractmethod
    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear console."""
        pass

    @abstractmethod
    def get_width(self) -> int:
        """Get console width."""
        pass

    @abstractmethod
    def get_height(self) -> int:
        """Get console height."""
        pass


class Console(BaseConsole):
    """Default console implementation."""

    def __init__(self, config: ConsoleConfig | None = None) -> None:
        """Initialize console."""
        super().__init__()
        self.config = config or ConsoleConfig()
        self._console: RichConsole = RichConsole(
            stderr=self.config.stderr,
            file=self.config.file,
            force_terminal=self.config.force_terminal,
            color_system=self.config.color_system,
            record=self.config.record,
            markup=self.config.markup,
            emoji=self.config.emoji,
            highlight=self.config.highlight,
            width=self.config.width,
            height=self.config.height,
        )
        self._width = self.config.width
        self._height = self.config.height

    @property
    def width(self) -> int:
        """Get console width."""
        return self._width or self._console.width or 80

    @property
    def height(self) -> int:
        """Get console height."""
        return self._height or self._console.height or 24

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console."""
        self._console.print(*args, **kwargs)

    def clear(self) -> None:
        """Clear console."""
        self._console.clear()

    def get_width(self) -> int:
        """Get console width."""
        return self.width

    def get_height(self) -> int:
        """Get console height."""
        return self.height

    def info(self, message: str) -> None:
        """Print info message."""
        self.print(f"ℹ️ {message}", style=Style(color="blue"))

    def success(self, message: str) -> None:
        """Print success message."""
        self.print(f"✅ {message}", style=Style(color="green"))

    def warning(self, message: str) -> None:
        """Print warning message."""
        self.print(f"⚠️ {message}", style=Style(color="yellow"))

    def error(self, message: str) -> None:
        """Print error message."""
        self.print(f"❌ {message}", style=Style(color="red"))
