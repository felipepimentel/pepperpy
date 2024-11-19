"""Console interface implementation"""

from dataclasses import dataclass
from typing import Any

from rich.console import Console as RichConsole


@dataclass
class ConsoleConfig:
    """Console configuration"""

    # Add config options as needed
    pass


class Console:
    """Console interface for terminal interactions"""

    def __init__(self, config: ConsoleConfig | None = None) -> None:
        self.config = config or ConsoleConfig()
        self._console = RichConsole()

    async def print(self, content: Any, **kwargs: Any) -> None:
        """Print content to console"""
        self._console.print(content, **kwargs)
