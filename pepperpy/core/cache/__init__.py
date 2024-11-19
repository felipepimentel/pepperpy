"""Core cache module"""

from .base import BaseCache, CacheProvider
from .distributed import DistributedCache
from .exceptions import CacheConnectionError, CacheError, CacheKeyError, CacheValueError
from .lru import LRUCache
from .memory import MemoryCache
from .strategies import CacheStrategy, LFUStrategy, LRUStrategy
from .vector import VectorCache

__all__ = [
    # Classes base
    "BaseCache",
    "CacheProvider",
    "CacheStrategy",
    # Implementações
    "MemoryCache",
    "LRUCache",
    "DistributedCache",
    "VectorCache",
    # Estratégias
    "LRUStrategy",
    "LFUStrategy",
    # Exceções
    "CacheError",
    "CacheConnectionError",
    "CacheKeyError",
    "CacheValueError",
]
