"""Base application module."""

from abc import ABC, abstractmethod
from typing import Any


class BaseApp(ABC):
    """Base application interface."""

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
