"""SentenceTransformers embedding provider"""

from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from ..exceptions import EmbeddingError
from ..types import EmbeddingVector
from .base import BaseEmbeddingProvider


class SentenceTransformersProvider(BaseEmbeddingProvider):
    """Provider using sentence-transformers models"""

    async def initialize(self) -> None:
        """Initialize the model"""
        try:
            self._model = SentenceTransformer(self.config.model)
        except Exception as e:
            raise EmbeddingError(f"Failed to load model: {str(e)}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self._model = None

    async def embed_text(self, text: str) -> EmbeddingVector:
        """Generate embedding for text"""
        if not self._model:
            raise EmbeddingError("Model not initialized")

        try:
            vector = self._model.encode(text)
            if self.config.normalize:
                vector = vector / np.linalg.norm(vector)

            return EmbeddingVector(vector=vector, text=text, model=self.config.model)
        except Exception as e:
            raise EmbeddingError(f"Embedding generation failed: {str(e)}", cause=e)

    async def embed_batch(self, texts: List[str]) -> List[EmbeddingVector]:
        """Generate embeddings for multiple texts"""
        if not self._model:
            raise EmbeddingError("Model not initialized")

        try:
            vectors = self._model.encode(texts)
            if self.config.normalize:
                vectors = vectors / np.linalg.norm(vectors, axis=1)[:, np.newaxis]

            return [
                EmbeddingVector(vector=vector, text=text, model=self.config.model)
                for vector, text in zip(vectors, texts)
            ]
        except Exception as e:
            raise EmbeddingError(f"Batch embedding failed: {str(e)}", cause=e)
