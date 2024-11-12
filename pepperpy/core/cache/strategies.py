"""Cache strategies implementation"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheStrategy(ABC):
    """Base class for cache strategies"""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cache value"""
        pass


class LRUStrategy(CacheStrategy):
    """Least Recently Used cache strategy"""

    pass


class LFUStrategy(CacheStrategy):
    """Least Frequently Used cache strategy"""

    pass
