"""In-memory cache implementation"""

from typing import Any, Optional

from .base import BaseCache


class MemoryCache(BaseCache):
    """Simple in-memory cache implementation"""

    def __init__(self) -> None:
        super().__init__()
        self._cache: dict[str, Any] = {}

    async def _initialize(self) -> None:
        """Initialize cache"""
        self._cache.clear()
        self._initialized = True

    async def _cleanup(self) -> None:
        """Cleanup cache"""
        self._cache.clear()
        self._initialized = False

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        self._ensure_initialized()
        return self._cache.get(key)

    async def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        self._ensure_initialized()
        self._cache[key] = value

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        self._ensure_initialized()
        self._cache.pop(key, None)

    async def clear(self) -> None:
        """Clear cache"""
        self._ensure_initialized()
        self._cache.clear()
