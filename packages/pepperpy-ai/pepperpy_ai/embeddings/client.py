"""Embedding client module"""

from typing import List, Sequence

from bko.ai.embeddings.base import BaseEmbeddingProvider
from bko.ai.embeddings.types import EmbeddingResult


class EmbeddingClient:
    """Client for embedding operations"""

    def __init__(self, provider: BaseEmbeddingProvider) -> None:
        """Initialize client"""
        self._provider = provider
        self._initialized = False

    @property
    def provider(self) -> BaseEmbeddingProvider:
        """Get provider"""
        return self._provider

    @property
    def is_initialized(self) -> bool:
        """Check if client is initialized"""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize client"""
        await self._provider.initialize()
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup client"""
        await self._provider.cleanup()
        self._initialized = False

    async def embed(self, text: str) -> EmbeddingResult:
        """Get embedding for text"""
        if not self._initialized:
            raise RuntimeError("Client not initialized")

        # Get raw embedding vector
        raw_vector = await self._provider.embed(text)

        # Create result with the raw vector
        return EmbeddingResult(
            embeddings=raw_vector,  # raw_vector is already List[float]
            dimensions=len(raw_vector),
            text=text,
            model=self._provider.config.model_name,
        )

    async def embed_batch(
        self, texts: Sequence[str], batch_size: int = 32
    ) -> List[EmbeddingResult]:
        """Get embeddings for multiple texts"""
        if not self._initialized:
            raise RuntimeError("Client not initialized")

        # Get raw embedding vectors
        text_list = list(texts)
        raw_vectors = await self._provider.embed_batch(text_list)

        # Create results with raw vectors
        return [
            EmbeddingResult(
                embeddings=vector,  # vector is already List[float]
                dimensions=len(vector),
                text=text,
                model=self._provider.config.model_name,
            )
            for vector, text in zip(raw_vectors, text_list)
        ]
