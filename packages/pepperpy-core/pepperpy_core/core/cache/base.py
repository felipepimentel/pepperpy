"""Base cache implementation"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class BaseCache(ABC, Generic[K, V]):
    """Base cache implementation"""

    def __init__(self) -> None:
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize cache"""
        if not self._initialized:
            await self._initialize()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup cache"""
        if self._initialized:
            await self._cleanup()
            self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if cache is initialized"""
        return self._initialized

    def _ensure_initialized(self) -> None:
        """Ensure cache is initialized"""
        if not self._initialized:
            raise RuntimeError("Cache not initialized")

    @abstractmethod
    async def _initialize(self) -> None:
        """Initialize cache implementation"""
        ...

    @abstractmethod
    async def _cleanup(self) -> None:
        """Cleanup cache implementation"""
        ...

    @abstractmethod
    async def get(self, key: K) -> V | None:
        """Get value from cache"""
        ...

    @abstractmethod
    async def set(self, key: K, value: V) -> None:
        """Set value in cache"""
        ...

    @abstractmethod
    async def delete(self, key: K) -> None:
        """Delete value from cache"""
        ...

    @abstractmethod
    async def clear(self) -> None:
        """Clear cache"""
        ...


class CacheProvider(ABC):
    """Cache provider interface"""

    def __init__(self) -> None:
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize provider"""
        if not self._initialized:
            await self._initialize()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup provider"""
        if self._initialized:
            await self._cleanup()
            self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized"""
        return self._initialized

    def _ensure_initialized(self) -> None:
        """Ensure provider is initialized"""
        if not self._initialized:
            raise RuntimeError("Provider not initialized")

    @abstractmethod
    async def _initialize(self) -> None:
        """Initialize provider implementation"""
        ...

    @abstractmethod
    async def _cleanup(self) -> None:
        """Cleanup provider implementation"""
        ...

    @abstractmethod
    async def create_cache(self, name: str) -> BaseCache[Any, Any]:
        """Create cache instance"""
        ...

    @abstractmethod
    async def delete_cache(self, name: str) -> None:
        """Delete cache instance"""
        ...

    @abstractmethod
    def get_cache(self) -> BaseCache[Any, Any]:
        """Get cache instance"""
        ...
