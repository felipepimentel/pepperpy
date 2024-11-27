"""Distributed cache implementation"""

import json
from typing import Any, Optional

import redis
from bko.core.exceptions import PepperPyError

from .base import BaseCache


class DistributedCache(BaseCache[str, Any]):
    """Distributed cache implementation"""

    def __init__(self, url: str, prefix: str = "test", ttl: Optional[int] = 3600) -> None:
        """Initialize distributed cache"""
        super().__init__()
        self._url = url
        self._prefix = prefix
        self._ttl = ttl
        self._client: Optional[redis.Redis] = None

    async def _initialize(self) -> None:
        """Initialize cache"""
        try:
            self._client = redis.Redis.from_url(self._url, decode_responses=True)
            # Test connection
            self._client.ping()
            self._initialized = True
        except Exception as e:
            self._client = None
            raise PepperPyError("Failed to connect to Redis", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup cache"""
        if self._client:
            try:
                self._client.close()
            except Exception:
                pass  # Ignore cleanup errors
            self._client = None
        self._initialized = False

    def _get_key(self, key: str) -> str:
        """Get prefixed key"""
        return f"{self._prefix}:{key}"

    async def get(self, key: str) -> Any | None:
        """Get value from cache"""
        self._ensure_initialized()
        if not self._client:
            raise PepperPyError("Redis client not available")

        try:
            value = self._client.get(self._get_key(key))
            if value is None:
                return None
            try:
                if isinstance(value, (str, bytes, bytearray)):
                    return json.loads(value)
                return value  # For mock testing
            except json.JSONDecodeError as e:
                raise PepperPyError("Failed to deserialize value", cause=e)
        except Exception as e:
            if isinstance(e, PepperPyError):
                raise
            raise PepperPyError("Failed to get value from cache", cause=e)

    async def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        self._ensure_initialized()
        if not self._client:
            raise PepperPyError("Redis client not available")

        try:
            try:
                serialized = json.dumps(value)
            except TypeError as e:
                raise PepperPyError("Failed to serialize value", cause=e)

            self._client.set(self._get_key(key), serialized, ex=self._ttl)
        except Exception as e:
            if isinstance(e, PepperPyError):
                raise
            raise PepperPyError("Failed to set value in cache", cause=e)

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        self._ensure_initialized()
        if not self._client:
            raise PepperPyError("Redis client not available")

        try:
            self._client.delete(self._get_key(key))
        except Exception as e:
            raise PepperPyError("Failed to delete value from cache", cause=e)

    async def clear(self) -> None:
        """Clear cache"""
        self._ensure_initialized()
        if not self._client:
            raise PepperPyError("Redis client not available")

        try:
            self._client.flushdb()
        except Exception as e:
            raise PepperPyError("Failed to clear cache", cause=e)
