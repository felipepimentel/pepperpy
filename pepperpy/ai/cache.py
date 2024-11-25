"""AI cache implementation"""

import hashlib
import json
from typing import Any

from pepperpy.core.cache.base import BaseCache
from pepperpy.core.exceptions import PepperPyError

from .types import AIResponse


class AICache:
    """AI cache implementation"""

    def __init__(self, cache: BaseCache) -> None:
        """Initialize cache"""
        self._cache = cache
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize cache"""
        if not self._initialized:
            await self._cache.initialize()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup cache"""
        if self._initialized:
            await self._cache.cleanup()
            self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if cache is initialized"""
        return self._initialized

    def generate_key(self, prompt: str, **kwargs: Any) -> str:
        """Generate cache key"""
        # Combine prompt and kwargs into a string
        key_data = {
            "prompt": prompt,
            **kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True)
        
        # Generate hash
        return hashlib.sha256(key_str.encode()).hexdigest()

    async def get(self, key: str) -> AIResponse | None:
        """Get value from cache"""
        try:
            return await self._cache.get(key)
        except Exception as e:
            raise PepperPyError("Cache operation failed", cause=e)

    async def set(self, key: str, value: AIResponse) -> None:
        """Set value in cache"""
        try:
            await self._cache.set(key, value)
        except Exception as e:
            raise PepperPyError("Cache operation failed", cause=e)

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        try:
            await self._cache.delete(key)
        except Exception as e:
            raise PepperPyError("Cache operation failed", cause=e)

    async def clear(self) -> None:
        """Clear cache"""
        try:
            await self._cache.clear()
        except Exception as e:
            raise PepperPyError("Cache operation failed", cause=e) 