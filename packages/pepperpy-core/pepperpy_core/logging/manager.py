"""Logging manager module."""

from abc import ABC, abstractmethod
from typing import Any

from .config import LogConfig


class LogManager(ABC):
    """Abstract log manager."""

    def __init__(self, config: LogConfig) -> None:
        """Initialize log manager.

        Args:
            config: Log configuration
        """
        self.config = config
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize log manager."""
        if self._initialized:
            return
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup log manager."""
        if not self._initialized:
            return
        self._initialized = False

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        pass

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        pass
