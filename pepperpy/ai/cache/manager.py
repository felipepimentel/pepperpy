"""Cache manager implementation"""

from typing import Any, Dict, List, Optional

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import CacheConfig
from .exceptions import CacheError
from .memory import MemoryCache
from .types import VectorEntry
from .vector import VectorCache


class CacheManager(BaseModule):
    """Manager for different cache types"""

    def __init__(self, config: Optional[CacheConfig] = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="cache",
            version="1.0.0",
            description="AI caching functionality",
            dependencies=[],
            config=config.dict() if config else {},
        )
        self._memory_cache = None
        self._vector_cache = None

    async def _setup(self) -> None:
        """Initialize cache components"""
        try:
            self._memory_cache = MemoryCache(default_ttl=self.config.get("default_ttl", 3600))

            if self.config.get("vector_enabled", True):
                self._vector_cache = VectorCache(self.config)
                await self._vector_cache.initialize()

        except Exception as e:
            raise CacheError("Failed to initialize cache", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup cache resources"""
        if self._memory_cache:
            await self._memory_cache.cleanup()
        if self._vector_cache:
            await self._vector_cache.cleanup()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from memory cache"""
        if not self._memory_cache:
            raise CacheError("Memory cache not initialized")
        return await self._memory_cache.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in memory cache"""
        if not self._memory_cache:
            raise CacheError("Memory cache not initialized")
        await self._memory_cache.set(key, value, ttl)

    async def vector_search(
        self, vector: Any, limit: int = 1, threshold: float = 0.8
    ) -> List[VectorEntry]:
        """Search for similar vectors"""
        if not self._vector_cache:
            raise CacheError("Vector cache not initialized")
        return await self._vector_cache.search(vector, limit, threshold)

    async def vector_add(self, key: str, vector: Any, metadata: Optional[Dict] = None) -> None:
        """Add vector to cache"""
        if not self._vector_cache:
            raise CacheError("Vector cache not initialized")
        await self._vector_cache.add(key, vector, metadata)
