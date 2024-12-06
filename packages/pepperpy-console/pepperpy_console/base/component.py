"""Base component module."""

from abc import ABC, abstractmethod
from typing import Any


class BaseComponent(ABC):
    """Base class for console components."""

    def __init__(self) -> None:
        """Initialize component."""
        self._initialized = False

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize component.

        This method should be called before using the component.
        """
        self._initialized = True

    @abstractmethod
    async def render(self) -> Any:
        """Render component.

        Returns:
            Component rendered content
        """
        if not self._initialized:
            await self.initialize()

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup component resources."""
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure component is initialized.

        Raises:
            RuntimeError: If component is not initialized
        """
        if not self._initialized:
            raise RuntimeError("Component not initialized")
