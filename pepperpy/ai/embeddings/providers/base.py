"""Base embeddings provider implementation"""

from abc import ABC, abstractmethod

from ..config import EmbeddingConfig
from ..types import EmbeddingVector


class BaseEmbeddingProvider(ABC):
    """Base class for embedding providers"""

    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self._model = None

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""

    @abstractmethod
    async def embed_text(self, text: str) -> EmbeddingVector:
        """Generate embedding for text"""

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[EmbeddingVector]:
        """Generate embeddings for multiple texts"""
