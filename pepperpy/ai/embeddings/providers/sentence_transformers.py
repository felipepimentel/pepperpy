"""Sentence Transformers embedding provider"""

from typing import List, Optional, Sequence, cast

import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer

from pepperpy.ai.embeddings.base import BaseEmbeddingProvider
from pepperpy.ai.embeddings.exceptions import EmbeddingError


class SentenceTransformerProvider(BaseEmbeddingProvider):
    """Provider for sentence-transformers embeddings"""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize provider"""
        super().__init__(*args, **kwargs)
        self._model: Optional[SentenceTransformer] = None
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized"""
        return self._initialized

    @property
    def model(self) -> Optional[SentenceTransformer]:
        """Get model instance"""
        return self._model

    async def initialize(self) -> None:
        """Initialize provider"""
        try:
            self._model = SentenceTransformer(self.config.model_name)
            self._initialized = True
        except Exception as e:
            raise EmbeddingError("Failed to load model", cause=e)

    async def cleanup(self) -> None:
        """Cleanup provider"""
        self._model = None
        self._initialized = False

    async def embed(self, text: str) -> List[float]:
        """Get embedding for text"""
        if not self._initialized or not self._model:
            raise RuntimeError("Provider not initialized")

        if not text:
            raise EmbeddingError("Empty text")

        try:
            # Encode text and get first (and only) embedding
            embedding = cast(NDArray[np.float32], self._model.encode([text])[0])

            # Validate dimension
            if len(embedding) != self.config.dimension:
                raise EmbeddingError(
                    f"Embedding dimension mismatch: expected {self.config.dimension}, got {len(embedding)}"
                )

            # Convert to list of floats
            return embedding.tolist()
        except EmbeddingError:
            raise
        except Exception as e:
            raise EmbeddingError("Failed to generate embedding", cause=e)

    async def embed_batch(self, texts: Sequence[str]) -> List[List[float]]:
        """Get embeddings for multiple texts"""
        if not self._initialized or not self._model:
            raise RuntimeError("Provider not initialized")

        if not texts:
            raise EmbeddingError("Empty batch")

        try:
            # Convert to list for consistent handling
            text_list = list(texts)

            # Encode all texts at once
            embeddings = cast(NDArray[np.float32], self._model.encode(text_list))

            # Validate dimensions
            if embeddings.shape[1] != self.config.dimension:
                raise EmbeddingError(
                    f"Embedding dimension mismatch: expected {self.config.dimension}, got {embeddings.shape[1]}"
                )

            # Convert to list of lists
            return embeddings.tolist()
        except EmbeddingError:
            raise
        except Exception as e:
            raise EmbeddingError("Failed to generate embeddings", cause=e)
