"""Cache module"""

from .base import BaseCache, CacheConfig, CacheEntry
from .manager import CacheManager
from .memory import MemoryCache

__all__ = [
    "BaseCache",
    "CacheConfig",
    "CacheEntry",
    "CacheManager",
    "MemoryCache",
]

try:
    from .distributed import DistributedCache

    __all__.append("DistributedCache")
except ImportError:
    pass
