"""Base embedding provider module"""

from abc import ABC, abstractmethod
from typing import List, Sequence

from pepperpy.ai.embeddings.config import EmbeddingConfig
from pepperpy.ai.embeddings.types import EmbeddingVector


class BaseEmbeddingProvider(ABC):
    """Base class for embedding providers"""

    def __init__(self, config: EmbeddingConfig) -> None:
        """Initialize provider

        Args:
            config: Provider configuration
        """
        self._config = config
        self._initialized = False

    @property
    def config(self) -> EmbeddingConfig:
        """Get provider configuration"""
        return self._config

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized"""
        return self._initialized

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""
        raise NotImplementedError

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider"""
        raise NotImplementedError

    @abstractmethod
    async def embed(self, text: str) -> EmbeddingVector:
        """Get embedding for text

        Args:
            text: Text to embed

        Returns:
            List of embedding values

        Raises:
            RuntimeError: If provider not initialized
            EmbeddingError: If embedding fails
        """
        raise NotImplementedError

    @abstractmethod
    async def embed_batch(self, texts: Sequence[str]) -> List[EmbeddingVector]:
        """Get embeddings for multiple texts

        Args:
            texts: Texts to embed

        Returns:
            List of embedding values for each text

        Raises:
            RuntimeError: If provider not initialized
            EmbeddingError: If embedding fails
        """
        raise NotImplementedError
