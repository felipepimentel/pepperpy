"""Base console application"""

from abc import ABC, abstractmethod

from .config import ConsoleConfig


class ConsoleApp(ABC):
    """Abstract base class for console applications"""

    def __init__(self, config: ConsoleConfig | None = None):
        self.config = config or ConsoleConfig()

    @abstractmethod
    async def start(self) -> None:
        """Start the application"""

    @abstractmethod
    async def stop(self) -> None:
        """Stop the application"""
