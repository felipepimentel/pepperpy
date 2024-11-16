"""Console module for terminal UI"""

from typing import Any

from rich.console import Console as RichConsole


class Console:
    """Console wrapper for Rich console"""

    def __init__(self):
        self._console = RichConsole()

    def clear(self) -> None:
        """Clear console screen"""
        self._console.clear()

    async def print(self, content: Any) -> None:
        """Print content to console"""
        if hasattr(content, "render"):
            rendered_content = await content.render()
            self._console.print(rendered_content)
        else:
            self._console.print(content)

    def success(self, message: str) -> None:
        """Print success message"""
        self._console.print(f"✅ {message}", style="green bold")

    def error(self, message: str) -> None:
        """Print error message"""
        self._console.print(f"❌ {message}", style="red bold")

    def warning(self, message: str) -> None:
        """Print warning message"""
        self._console.print(f"⚠️ {message}", style="yellow bold")

    def info(self, message: str) -> None:
        """Print info message"""
        self._console.print(f"ℹ️ {message}", style="blue bold")
