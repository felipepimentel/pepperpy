"""Distributed cache implementation"""

from typing import Any, Optional

import msgpack
from redis import asyncio as aioredis

from ..exceptions import CoreError
from .strategies import CacheStrategy


class RedisCache(CacheStrategy):
    """Redis-based distributed cache"""

    def __init__(
        self, host: str = "localhost", port: int = 6379, password: Optional[str] = None, db: int = 0
    ):
        self._redis = None
        self._config = {"host": host, "port": port, "password": password, "db": db}

    async def initialize(self) -> None:
        """Initialize Redis connection"""
        try:
            self._redis = await aioredis.create_redis_pool(**self._config)
        except Exception as e:
            raise CoreError(f"Failed to initialize Redis cache: {str(e)}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup Redis connection"""
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        try:
            value = await self._redis.get(key)
            if value:
                return msgpack.unpackb(value, raw=False)
            return None
        except Exception as e:
            raise CoreError(f"Redis get failed: {str(e)}", cause=e)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in Redis"""
        try:
            packed = msgpack.packb(value, use_bin_type=True)
            if ttl:
                await self._redis.setex(key, ttl, packed)
            else:
                await self._redis.set(key, packed)
        except Exception as e:
            raise CoreError(f"Redis set failed: {str(e)}", cause=e)

    async def delete(self, key: str) -> None:
        """Delete value from Redis"""
        try:
            await self._redis.delete(key)
        except Exception as e:
            raise CoreError(f"Redis delete failed: {str(e)}", cause=e)

    async def clear(self) -> None:
        """Clear all values"""
        try:
            await self._redis.flushdb()
        except Exception as e:
            raise CoreError(f"Redis clear failed: {str(e)}", cause=e)
