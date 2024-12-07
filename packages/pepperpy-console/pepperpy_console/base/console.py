"""Base console module."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Literal, TextIO

if TYPE_CHECKING:
    from rich.console import Console as ConsoleType
else:
    from rich._console import Console as ConsoleType

from rich.style import Style

from ..rich.types import RichConsoleProtocol

# Define valid color system types
ColorSystem = Literal["auto", "standard", "256", "truecolor", "windows"]


class ConsoleConfig:
    """Console configuration."""

    def __init__(self) -> None:
        """Initialize console configuration."""
        self.stderr: bool = False
        self.file: TextIO | None = None
        self.force_terminal: bool | None = None
        self.color_system: ColorSystem | None = "auto"
        self.record: bool = False
        self.markup: bool = True
        self.emoji: bool = True
        self.highlight: bool = True
        self.width: int | None = None
        self.height: int | None = None
        self.metadata: dict[str, Any] = {}

    def to_kwargs(self) -> dict[str, Any]:
        """Convert to rich console kwargs."""
        return {
            "stderr": self.stderr,
            "file": self.file,
            "force_terminal": self.force_terminal,
            "color_system": self.color_system,
            "record": self.record,
            "markup": self.markup,
            "emoji": self.emoji,
            "highlight": self.highlight,
            "width": self.width,
            "height": self.height,
        }


class BaseConsole(ABC):
    """Base console interface."""

    _console: RichConsoleProtocol

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
        self._console = ConsoleType(**self.config.to_kwargs())  # type: ignore
        self._width = self.config.width
        self._height = self.config.height

    @property
    def width(self) -> int:
        """Get console width."""
        console_width: int = getattr(self._console, "width", 80)
        return self._width or console_width or 80

    @property
    def height(self) -> int:
        """Get console height."""
        console_height: int = getattr(self._console, "height", 24)
        return self._height or console_height or 24

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
