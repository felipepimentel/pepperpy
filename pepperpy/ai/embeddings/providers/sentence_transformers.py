"""Sentence Transformers embedding provider"""

from typing import List, Union, cast

import numpy as np
import torch
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer

from ...exceptions import AIError
from ..config import EmbeddingConfig
from ..types import EmbeddingVector
from .base import BaseEmbeddingProvider


class SentenceTransformersProvider(BaseEmbeddingProvider):
    """Provider for Sentence Transformers embeddings"""

    def __init__(self, config: EmbeddingConfig):
        """Initialize provider with config

        Args:
            config: Embedding configuration
        """
        super().__init__(config)
        try:
            self.model = SentenceTransformer(config.model)
            # Get and validate model dimension
            dimension = self.model.get_sentence_embedding_dimension()
            if not isinstance(dimension, int) or dimension <= 0:
                raise AIError(f"Invalid model dimension: {dimension}")
            self.model_dimension = dimension
        except Exception as e:
            raise AIError(f"Failed to load model {config.model}: {str(e)}", cause=e)

    async def initialize(self) -> None:
        """Initialize provider"""
        pass

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        pass

    def _normalize_vector(
        self, vector: Union[torch.Tensor, NDArray[np.float32], List[torch.Tensor]]
    ) -> NDArray[np.float32]:
        """Normalize vector to numpy array"""
        if isinstance(vector, torch.Tensor):
            vector = vector.detach().cpu().numpy()
        elif isinstance(vector, list):
            vector = torch.stack(vector).detach().cpu().numpy()

        return cast(NDArray[np.float32], vector.astype(np.float32))

    async def embed_text(self, text: str) -> EmbeddingVector:
        """Generate embedding for text"""
        try:
            vector = self.model.encode(
                text,
                convert_to_tensor=True,
                normalize_embeddings=True,
            )
            normalized = self._normalize_vector(vector)
            return EmbeddingVector(vector=normalized, text=text)
        except Exception as e:
            raise AIError(f"Failed to generate embedding: {str(e)}", cause=e)

    async def embed_batch(self, texts: List[str]) -> List[EmbeddingVector]:
        """Generate embeddings for multiple texts"""
        try:
            vectors = self.model.encode(
                texts,
                convert_to_tensor=True,
                normalize_embeddings=True,
            )
            normalized = self._normalize_vector(vectors)
            return [EmbeddingVector(vector=vec, text=text) for vec, text in zip(normalized, texts)]
        except Exception as e:
            raise AIError(f"Failed to generate embeddings: {str(e)}", cause=e)
