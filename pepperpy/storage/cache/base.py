"""Base cache system."""
from typing import Any, Optional, Union
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import pickle

class CacheKey:
    """Cache key with namespace support."""
    
    def __init__(self, key: str, namespace: Optional[str] = None):
        self.key = key
        self.namespace = namespace
    
    def __str__(self) -> str:
        if self.namespace:
            return f"{self.namespace}:{self.key}"
        return self.key

class CacheEntry:
    """Cache entry with metadata."""
    
    def __init__(
        self,
        value: Any,
        expires_at: Optional[datetime] = None,
        metadata: Optional[dict] = None
    ):
        self.value = value
        self.expires_at = expires_at
        self.metadata = metadata or {}
        self.created_at = datetime.now()
    
    @property
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at
    
    def serialize(self) -> bytes:
        """Serialize entry for storage."""
        return pickle.dumps(self)
    
    @classmethod
    def deserialize(cls, data: bytes) -> 'CacheEntry':
        """Deserialize entry from storage."""
        return pickle.loads(data)

class BaseCache(ABC):
    """Base cache interface."""
    
    @abstractmethod
    async def get(
        self,
        key: Union[str, CacheKey],
        default: Any = None
    ) -> Any:
        """Get value from cache."""
        pass
    
    @abstractmethod
    async def set(
        self,
        key: Union[str, CacheKey],
        value: Any,
        ttl: Optional[int] = None,
        metadata: Optional[dict] = None
    ) -> None:
        """Set value in cache."""
        pass
    
    @abstractmethod
    async def delete(self, key: Union[str, CacheKey]) -> None:
        """Delete value from cache."""
        pass
    
    @abstractmethod
    async def clear(self, namespace: Optional[str] = None) -> None:
        """Clear cache entries."""
        pass
    
    async def get_or_set(
        self,
        key: Union[str, CacheKey],
        func: callable,
        ttl: Optional[int] = None,
        **kwargs
    ) -> Any:
        """Get value from cache or compute and store it."""
        value = await self.get(key)
        if value is None:
            value = await func(**kwargs)
            await self.set(key, value, ttl)
        return value 