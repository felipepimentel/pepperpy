"""Sentence Transformers embedding provider"""

from typing import List, Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field
from sentence_transformers import SentenceTransformer

from ...base.types import JsonDict
from ...exceptions import AIError
from ..base import EmbeddingProvider


class SentenceTransformersConfig(BaseModel):
    """Sentence Transformers configuration"""

    model_name: str = Field(default="all-MiniLM-L6-v2")
    device: str = Field(default="cpu")
    batch_size: int = Field(default=32, gt=0)
    normalize_embeddings: bool = Field(default=True)
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)


class SentenceTransformersProvider(EmbeddingProvider[SentenceTransformersConfig]):
    """Sentence Transformers provider implementation"""

    def __init__(self, config: SentenceTransformersConfig) -> None:
        super().__init__(config)
        self._model: Optional[SentenceTransformer] = None

    async def _initialize(self) -> None:
        """Initialize provider"""
        try:
            self._model = SentenceTransformer(
                self.config.model_name,
                device=self.config.device,
            )
        except Exception as e:
            raise AIError("Failed to initialize SentenceTransformer", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup provider"""
        self._model = None

    async def embed(self, text: str) -> List[float]:
        """Get embedding for text"""
        self._ensure_initialized()
        if not self._model:
            raise AIError("Model not initialized")

        try:
            embedding = self._model.encode(
                [text],
                batch_size=self.config.batch_size,
                normalize_embeddings=self.config.normalize_embeddings,
            )[0]
            return embedding.tolist()
        except Exception as e:
            raise AIError("Failed to generate embedding", cause=e)

    async def embed_batch(self, texts: Sequence[str]) -> List[List[float]]:
        """Get embeddings for multiple texts"""
        self._ensure_initialized()
        if not self._model:
            raise AIError("Model not initialized")

        try:
            embeddings = self._model.encode(
                texts,
                batch_size=self.config.batch_size,
                normalize_embeddings=self.config.normalize_embeddings,
            )
            return embeddings.tolist()
        except Exception as e:
            raise AIError("Failed to generate embeddings", cause=e)
