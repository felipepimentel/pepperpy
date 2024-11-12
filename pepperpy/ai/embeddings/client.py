"""Embeddings client implementation"""

from typing import List, Optional

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import EmbeddingConfig
from .exceptions import EmbeddingError
from .providers import get_provider
from .types import EmbeddingBatch, EmbeddingVector


class EmbeddingClient(BaseModule):
    """Client for text embedding operations"""

    def __init__(self, config: Optional[EmbeddingConfig] = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="embeddings",
            version="1.0.0",
            description="Text embedding operations",
            dependencies=[],
            config=config.dict() if config else {},
        )
        self._provider = None
        self._cache = None

    async def _setup(self) -> None:
        """Initialize embeddings provider"""
        try:
            self._provider = get_provider(self.config)
            await self._provider.initialize()

            if self.config.get("cache_enabled"):
                from pepperpy.ai.cache import CacheManager

                self._cache = CacheManager(self.config)
                await self._cache.initialize()

        except Exception as e:
            raise EmbeddingError("Failed to initialize embeddings", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup embeddings resources"""
        if self._provider:
            await self._provider.cleanup()
        if self._cache:
            await self._cache.cleanup()

    async def embed_text(self, text: str) -> EmbeddingVector:
        """Generate embedding for text"""
        if not self._provider:
            raise EmbeddingError("Embeddings provider not initialized")

        # Check cache first
        if self._cache:
            cached = await self._cache.get(text)
            if cached:
                return cached

        # Generate embedding
        vector = await self._provider.embed_text(text)

        # Cache result
        if self._cache:
            await self._cache.set(text, vector, ttl=self.config.get("cache_ttl"))

        return vector

    async def embed_batch(self, texts: List[str]) -> EmbeddingBatch:
        """Generate embeddings for multiple texts"""
        if not self._provider:
            raise EmbeddingError("Embeddings provider not initialized")

        vectors = []
        batch_size = self.config.get("batch_size", 32)

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_vectors = await self._provider.embed_batch(batch)
            vectors.extend(batch_vectors)

        return EmbeddingBatch(vectors=vectors, model=self.config["model"])
