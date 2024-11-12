"""Memory cache implementation with TTL support"""

import time
from collections import OrderedDict
from threading import Lock
from typing import Any, Dict, Optional

from ..exceptions import CoreError
from .strategies import CacheStrategy


class MemoryCache(CacheStrategy):
    """Thread-safe memory cache with TTL"""

    def __init__(self, max_size: int = 1000, cleanup_interval: int = 60):
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._max_size = max_size
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.time()
        self._lock = Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            with self._lock:
                self._maybe_cleanup()

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
            raise CoreError(f"Memory cache get failed: {str(e)}", cause=e)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        try:
            with self._lock:
                self._maybe_cleanup()

                # Remove oldest if at max size
                if len(self._cache) >= self._max_size:
                    self._cache.popitem(last=False)

                expires_at = time.time() + ttl if ttl else None
                self._cache[key] = {
                    "value": value,
                    "expires_at": expires_at,
                    "created_at": time.time(),
                }
                self._cache.move_to_end(key)
        except Exception as e:
            raise CoreError(f"Memory cache set failed: {str(e)}", cause=e)

    def _maybe_cleanup(self) -> None:
        """Cleanup expired entries if needed"""
        now = time.time()
        if now - self._last_cleanup > self._cleanup_interval:
            self._cleanup()
            self._last_cleanup = now

    def _cleanup(self) -> None:
        """Remove expired entries"""
        now = time.time()
        expired = [
            key
            for key, entry in self._cache.items()
            if entry.get("expires_at") and entry["expires_at"] <= now
        ]
        for key in expired:
            del self._cache[key]
