"""Base cache provider implementation"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..config import CacheConfig


class BaseCacheProvider(ABC):
    """Base class for cache providers"""

    def __init__(self, config: CacheConfig):
        self.config = config

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all values from cache"""
        pass
