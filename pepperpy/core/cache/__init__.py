"""Core cache module"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .distributed import DistributedCache
from .exceptions import CacheConnectionError, CacheError, CacheKeyError, CacheValueError
from .lru import LRUCache
from .memory import MemoryCache
from .strategies import CacheStrategy, LFUStrategy, LRUStrategy

KT = TypeVar("KT")
VT = TypeVar("VT")


class Cache(Generic[KT, VT], ABC):
    """Base cache interface"""

    @abstractmethod
    def get(self, key: KT) -> VT | None:
        """Get value from cache"""
        pass

    @abstractmethod
    def set(self, key: KT, value: VT, ttl: int | None = None) -> None:
        """Set value in cache"""
        pass

    @abstractmethod
    def delete(self, key: KT) -> None:
        """Delete value from cache"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all values from cache"""
        pass


# Criar instâncias padrão para uso direto
memory_cache = MemoryCache[str, Any]()
lru_cache = LRUCache[str, Any](capacity=1000)


__all__ = [
    # Classes base
    "Cache",
    "CacheStrategy",
    # Implementações
    "MemoryCache",
    "LRUCache",
    "DistributedCache",
    # Estratégias
    "LRUStrategy",
    "LFUStrategy",
    # Exceções
    "CacheError",
    "CacheConnectionError",
    "CacheKeyError",
    "CacheValueError",
    # Instâncias padrão
    "memory_cache",
    "lru_cache",
]
