"""Console implementation"""

from typing import Any

from rich.console import Console as RichConsole


class Console:
    """Console interface with async support"""

    def __init__(self) -> None:
        self._console = RichConsole()

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Synchronous print"""
        self._console.print(*args, **kwargs)

    def clear(self) -> None:
        """Clear console screen"""
        self._console.clear()

    def info(self, *args: Any, **kwargs: Any) -> None:
        """Print info message"""
        self._console.print("ℹ️", *args, **kwargs)

    def error(self, *args: Any, **kwargs: Any) -> None:
        """Print error message"""
        self._console.print("❌", *args, style="red", **kwargs)

    def success(self, *args: Any, **kwargs: Any) -> None:
        """Print success message"""
        self._console.print("✅", *args, style="green", **kwargs)

    def warning(self, *args: Any, **kwargs: Any) -> None:
        """Print warning message"""
        self._console.print("⚠️", *args, style="yellow", **kwargs)
