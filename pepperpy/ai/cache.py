"""AI module cache utilities"""

from typing import Any

from pepperpy.core.cache.base import BaseCache, CacheProvider
from pepperpy.core.cache.vector import VectorCache
from pepperpy.core.types import JsonDict

from .exceptions import AIError


class AICache:
    """AI cache manager"""

    def __init__(self, provider: CacheProvider) -> None:
        self.provider = provider
        self._embeddings_cache: VectorCache | None = None
        self._response_cache: BaseCache[str, Any] | None = None

    async def initialize(self, dimension: int = 1536) -> None:
        """Initialize AI caches"""
        try:
            # Cache para embeddings
            self._embeddings_cache = await self.provider.create_cache(
                "ai_embeddings",
                cache_type="vector",
                dimension=dimension
            )

            # Cache para respostas
            self._response_cache = await self.provider.create_cache(
                "ai_responses",
                cache_type="memory"
            )

        except Exception as e:
            raise AIError(f"Failed to initialize AI cache: {e}", cause=e)

    async def store_embedding(
        self,
        text: str,
        embedding: list[float],
        metadata: JsonDict | None = None
    ) -> None:
        """Store text embedding"""
        if not self._embeddings_cache:
            raise AIError("Embeddings cache not initialized")

        try:
            await self._embeddings_cache.set(text, embedding, metadata=metadata)
        except Exception as e:
            raise AIError(f"Failed to store embedding: {e}", cause=e)

    async def find_similar(
        self,
        embedding: list[float],
        limit: int = 10,
        threshold: float = 0.8
    ) -> list[tuple[str, float, JsonDict]]:
        """Find similar embeddings"""
        if not self._embeddings_cache:
            raise AIError("Embeddings cache not initialized")

        try:
            return await self._embeddings_cache.search_similar(
                embedding,
                limit=limit,
                threshold=threshold
            )
        except Exception as e:
            raise AIError(f"Similarity search failed: {e}", cause=e)

    async def cache_response(
        self,
        key: str,
        response: Any,
        ttl: int | None = None
    ) -> None:
        """Cache AI response"""
        if not self._response_cache:
            raise AIError("Response cache not initialized")

        try:
            await self._response_cache.set(key, response, ttl=ttl)
        except Exception as e:
            raise AIError(f"Failed to cache response: {e}", cause=e)

    async def get_cached_response(self, key: str) -> Any | None:
        """Get cached AI response"""
        if not self._response_cache:
            raise AIError("Response cache not initialized")

        try:
            return await self._response_cache.get(key)
        except Exception as e:
            raise AIError(f"Failed to get cached response: {e}", cause=e) 