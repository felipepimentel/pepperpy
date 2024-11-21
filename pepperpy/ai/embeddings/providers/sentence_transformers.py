"""Sentence transformers embedding provider"""

from sentence_transformers import SentenceTransformer

from ..config import EmbeddingConfig
from .base import EmbeddingProvider


class SentenceTransformersProvider(EmbeddingProvider):
    """Sentence transformers provider implementation"""

    def __init__(self, config: EmbeddingConfig) -> None:
        """Initialize provider"""
        super().__init__(config)
        self._model: SentenceTransformer | None = None

    async def _initialize(self) -> None:
        """Initialize provider"""
        self._model = SentenceTransformer(self.config.model_name)

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        self._model = None

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        if not self._model:
            raise RuntimeError("Provider not initialized")
        embedding = self._model.encode(text)
        return embedding.tolist()
