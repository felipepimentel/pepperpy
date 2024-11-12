"""Base console application"""

from abc import ABC, abstractmethod
from typing import Optional

from .config import ConsoleConfig


class ConsoleApp(ABC):
    """Abstract base class for console applications"""

    def __init__(self, config: Optional[ConsoleConfig] = None):
        self.config = config or ConsoleConfig()

    @abstractmethod
    async def start(self) -> None:
        """Start the application"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop the application"""
        pass
