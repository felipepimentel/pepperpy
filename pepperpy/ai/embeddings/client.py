"""Embedding client implementation"""

from typing import Any

from pepperpy.core.module import BaseModule

from .config import EmbeddingConfig
from .exceptions import EmbeddingError


class EmbeddingClient(BaseModule[EmbeddingConfig]):
    """Embedding client implementation"""

    def __init__(self, config: EmbeddingConfig) -> None:
        super().__init__(config)
        self._provider = None

    async def _initialize(self) -> None:
        """Initialize embedding client"""
        if not self.config:
            raise EmbeddingError("Configuration required")
        # Initialize provider
        self._provider = self._create_provider()
        await self._provider.initialize()

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        if self._provider:
            await self._provider.cleanup()

    def _create_provider(self) -> Any:
        """Create embedding provider"""
        if not self.config:
            raise EmbeddingError("Configuration required")
        # Provider creation logic here
        raise NotImplementedError
