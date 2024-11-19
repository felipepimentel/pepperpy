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

    async def print_async(self, *args: Any, **kwargs: Any) -> None:
        """Asynchronous print"""
        self._console.print(*args, **kwargs)

    def info(self, *args: Any, **kwargs: Any) -> None:
        """Print info message"""
        self._console.print("ℹ️", *args, **kwargs)

    async def info_async(self, *args: Any, **kwargs: Any) -> None:
        """Print info message asynchronously"""
        self._console.print("ℹ️", *args, **kwargs)

    def error(self, *args: Any, **kwargs: Any) -> None:
        """Print error message"""
        self._console.print("❌", *args, style="red", **kwargs)

    async def error_async(self, *args: Any, **kwargs: Any) -> None:
        """Print error message asynchronously"""
        self._console.print("❌", *args, style="red", **kwargs)

    def success(self, *args: Any, **kwargs: Any) -> None:
        """Print success message"""
        self._console.print("✅", *args, style="green", **kwargs)

    async def success_async(self, *args: Any, **kwargs: Any) -> None:
        """Print success message asynchronously"""
        self._console.print("✅", *args, style="green", **kwargs) 