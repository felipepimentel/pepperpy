"""Distributed cache implementation using Redis."""

from typing import Any

try:
    import redis  # type: ignore
    from redis.client import Redis as RedisClient  # type: ignore

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False
    redis = None
    RedisClient = None  # type: ignore

from ..exceptions import CacheError
from .base import BaseCache
from .config import CacheConfig


class RedisError(CacheError):
    """Redis specific error."""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class RedisCache(BaseCache[CacheConfig]):
    """Redis cache implementation."""

    def __init__(self, config: CacheConfig | None = None) -> None:
        """Initialize Redis cache.

        Args:
            config: Cache configuration

        Raises:
            RedisError: If Redis is not available
        """
        if not HAS_REDIS:
            raise RedisError(
                "Redis support requires additional dependencies. "
                "Please install with: pip install redis"
            )

        super().__init__(config or CacheConfig(name="redis-cache"))
        self._client: Any = None

    async def _setup(self) -> None:
        """Setup Redis connection."""
        try:
            if redis is not None:
                client = redis.Redis(
                    host=self.config.host,  # type: ignore
                    port=self.config.port,  # type: ignore
                    db=self.config.db,  # type: ignore
                    password=self.config.password,  # type: ignore
                    decode_responses=True,
                )
                # Test connection
                if not client.ping():
                    raise RedisError("Failed to ping Redis server")
                self._client = client
        except Exception as e:
            raise RedisError("Failed to connect to Redis", cause=e)

    async def _teardown(self) -> None:
        """Cleanup Redis connection."""
        if self._client is not None:
            await self._client.close()
            self._client = None

    async def get(self, key: str) -> Any:
        """Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cache value if found, None otherwise

        Raises:
            RedisError: If operation fails
        """
        try:
            if not self.is_initialized or self._client is None:
                await self.initialize()
            value = await self._client.get(key)  # type: ignore
            if value is None:
                return None
            return value
        except Exception as e:
            raise RedisError(f"Failed to get key {key}", cause=e)

    async def set(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Cache value

        Raises:
            RedisError: If operation fails
        """
        try:
            if not self.is_initialized or self._client is None:
                await self.initialize()
            await self._client.set(key, value, ex=int(self.config.ttl))  # type: ignore
        except Exception as e:
            raise RedisError(f"Failed to set key {key}", cause=e)

    async def delete(self, key: str) -> None:
        """Delete value from cache.

        Args:
            key: Cache key

        Raises:
            RedisError: If operation fails
        """
        try:
            if not self.is_initialized or self._client is None:
                await self.initialize()
            await self._client.delete(key)  # type: ignore
        except Exception as e:
            raise RedisError(f"Failed to delete key {key}", cause=e)

    async def clear(self) -> None:
        """Clear all values from cache.

        Raises:
            RedisError: If operation fails
        """
        try:
            if not self.is_initialized or self._client is None:
                await self.initialize()
            await self._client.flushdb()  # type: ignore
        except Exception as e:
            raise RedisError("Failed to clear cache", cause=e)
