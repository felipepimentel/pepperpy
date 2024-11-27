"""Base embedding provider module"""

from abc import ABC, abstractmethod
from typing import List, Sequence

from bko.ai.embeddings.config import EmbeddingConfig
from bko.ai.embeddings.types import EmbeddingResult


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
    async def embed(self, text: str) -> List[float]:
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
    async def embed_batch(self, texts: Sequence[str]) -> List[List[float]]:
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

    async def get_embedding(self, text: str) -> EmbeddingResult:
        """Get embedding result for text

        Args:
            text: Text to embed

        Returns:
            Embedding result with metadata

        Raises:
            RuntimeError: If provider not initialized
            EmbeddingError: If embedding fails
        """
        embeddings = await self.embed(text)
        return EmbeddingResult(
            embeddings=embeddings,
            dimensions=len(embeddings),
            text=text,
            model=self.config.model_name,
        )

    async def get_embeddings(self, texts: Sequence[str]) -> List[EmbeddingResult]:
        """Get embedding results for multiple texts

        Args:
            texts: Texts to embed

        Returns:
            List of embedding results with metadata

        Raises:
            RuntimeError: If provider not initialized
            EmbeddingError: If embedding fails
        """
        embeddings = await self.embed_batch(texts)
        return [
            EmbeddingResult(
                embeddings=embedding,
                dimensions=len(embedding),
                text=text,
                model=self.config.model_name,
            )
            for embedding, text in zip(embeddings, texts)
        ]
