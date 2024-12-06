"""Base database engine module."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from pepperpy_core.exceptions import PepperpyError


class DatabaseError(PepperpyError):
    """Database specific error."""

    pass


ConfigT = TypeVar("ConfigT")


@dataclass
class BaseEngineConfig:
    """Base configuration for database engines."""

    name: str = ""
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseEngine(Generic[ConfigT], ABC):
    """Base database engine implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize engine.

        Args:
            config: Engine configuration
        """
        self.config = config
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if engine is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize engine."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup engine resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure engine is initialized."""
        if not self._initialized:
            raise RuntimeError("Engine not initialized")

    @abstractmethod
    async def _setup(self) -> None:
        """Setup engine resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown engine resources."""
        pass

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get engine statistics.

        Returns:
            Engine statistics
        """
        pass
