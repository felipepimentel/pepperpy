"""Base provider implementation."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Generic, TypeVar

from ..ai_types import AIResponse
from .config import ProviderConfig

ConfigT = TypeVar("ConfigT", bound=ProviderConfig)


class BaseProvider(Generic[ConfigT], ABC):
    """Base provider implementation."""

    def __init__(self, config: ConfigT) -> None:
        """Initialize provider.

        Args:
            config: Provider configuration
        """
        self.config = config
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized."""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize provider."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup provider resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    @abstractmethod
    async def _setup(self) -> None:
        """Setup provider resources."""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown provider resources."""
        pass

    @abstractmethod
    async def complete(self, prompt: str) -> AIResponse:
        """Complete prompt."""
        pass

    @abstractmethod
    async def stream(self, prompt: str) -> AsyncGenerator[AIResponse, None]:
        """Stream responses."""
        pass
