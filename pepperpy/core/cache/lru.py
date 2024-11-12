"""LRU cache implementation"""

import time
from collections import OrderedDict
from typing import Any, Dict, Optional

from ..exceptions import CoreError
from .strategies import CacheStrategy


class LRUCache(CacheStrategy):
    """Least Recently Used cache implementation"""

    def __init__(self, max_size: int = 1000):
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._max_size = max_size

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if key not in self._cache:
                return None

            entry = self._cache[key]
            if entry.get("expires_at") and time.time() > entry["expires_at"]:
                del self._cache[key]
                return None

            # Move to end (most recently used)
            self._cache.move_to_end(key)
            return entry["value"]
        except Exception as e:
            raise CoreError(f"LRU cache get failed: {str(e)}", cause=e)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        try:
            # Remove oldest if at max size
            if len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)

            expires_at = time.time() + ttl if ttl else None
            self._cache[key] = {"value": value, "expires_at": expires_at}
            self._cache.move_to_end(key)
        except Exception as e:
            raise CoreError(f"LRU cache set failed: {str(e)}", cause=e)

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        try:
            if key in self._cache:
                del self._cache[key]
        except Exception as e:
            raise CoreError(f"LRU cache delete failed: {str(e)}", cause=e)

    async def clear(self) -> None:
        """Clear all values"""
        try:
            self._cache.clear()
        except Exception as e:
            raise CoreError(f"LRU cache clear failed: {str(e)}", cause=e)
