"""Base cache implementation"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from ..base.types import JsonDict
from ..utils.datetime import utc_now


@dataclass
class CacheConfig:
    """Cache configuration"""

    default_ttl: int = 3600  # 1 hour
    max_size: int = 1000
    cleanup_interval: int = 60  # 1 minute
    prefix: str = ""
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class CacheEntry:
    """Cache entry"""

    key: str
    value: Any
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=utc_now)
    ttl: Optional[int] = None
    metadata: JsonDict = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        """Check if entry is expired"""
        return self.expires_at is not None and utc_now() > self.expires_at


class BaseCache(ABC):
    """Base cache interface"""

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
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        ...

    @abstractmethod
    async def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
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
    async def create_cache(self, name: str) -> BaseCache:
        """Create cache instance"""
        ...

    @abstractmethod
    async def delete_cache(self, name: str) -> None:
        """Delete cache instance"""
        ...

    @abstractmethod
    def get_cache(self) -> BaseCache:
        """Get cache instance"""
        ...


__all__ = [
    "BaseCache",
    "CacheConfig",
    "CacheEntry",
]
