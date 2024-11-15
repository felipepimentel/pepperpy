"""Base embedding provider implementation"""

from abc import ABC, abstractmethod

from .types import EmbeddingVector


class BaseEmbeddingProvider(ABC):
    """Base class for embedding providers"""

    @abstractmethod
    def embed(self, text: str) -> EmbeddingVector:
        """
        Generate embedding for text

        Args:
            text: Text to embed

        Returns:
            EmbeddingVector: Generated embedding

        """

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[EmbeddingVector]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of texts to embed

        Returns:
            List[EmbeddingVector]: Generated embeddings

        """
