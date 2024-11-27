"""Distributed cache implementation using Redis"""

import warnings
from typing import Any

try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    warnings.warn(
        "Redis is not installed. To use DistributedCache, install pepperpy-core[redis]",
        ImportWarning,
        stacklevel=2,
    )

from .base import BaseCache


class DistributedCache(BaseCache):
    """Redis-based distributed cache implementation"""

    def __init__(self, url: str, **kwargs: Any) -> None:
        """Initialize Redis cache

        Args:
            url: Redis connection URL
            **kwargs: Additional Redis connection options

        Raises:
            ImportError: If Redis is not installed
        """
        if not REDIS_AVAILABLE:
            raise ImportError("Redis is not installed. Please install pepperpy-core[redis] first.")

        self.client = redis.from_url(url, **kwargs)
        self._initialized = False

    async def _initialize(self) -> None:
        """Initialize cache connection"""
        try:
            await self.client.ping()
            self._initialized = True
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redis: {e}")

    async def _cleanup(self) -> None:
        """Cleanup cache connection"""
        if self._initialized:
            await self.client.close()
            self._initialized = False
