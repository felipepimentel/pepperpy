"""Base cache implementation"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


class BaseCache(Generic[KT, VT], ABC):
    """Base cache interface"""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize cache"""
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: KT, value: VT, **kwargs: Any) -> None:
        """Set value in cache"""
        raise NotImplementedError

    async def get(self, key: KT) -> VT | None:
        """Get value from cache"""
        raise NotImplementedError

    @abstractmethod
    async def clear(self) -> None:
        """Clear cache"""
        raise NotImplementedError

    async def delete(self, key: KT) -> None:
        """Delete value from cache"""
        raise NotImplementedError


class CacheProvider(ABC):
    """Cache provider interface"""

    @abstractmethod
    async def create_cache(self, name: str, **config: Any) -> BaseCache[Any, Any]:
        """Create cache instance"""
        raise NotImplementedError

    @abstractmethod
    async def get_cache(self, name: str) -> BaseCache[Any, Any]:
        """Get existing cache"""
        raise NotImplementedError

    @abstractmethod
    async def delete_cache(self, name: str) -> None:
        """Delete cache"""
        raise NotImplementedError
