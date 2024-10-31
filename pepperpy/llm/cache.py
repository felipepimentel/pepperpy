"""Cache implementation for LLM responses."""
from typing import Optional, Dict, Any
import hashlib
import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class CacheEntry:
    """Represents a cached LLM response."""
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    expires_at: Optional[datetime] = None

    def is_expired(self) -> bool:
        """Check if the cache entry has expired."""
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at

class BaseCache(ABC):
    """Base class for LLM response caching."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[CacheEntry]:
        """Retrieve a cached response."""
        pass
    
    @abstractmethod
    def set(
        self, 
        key: str, 
        entry: CacheEntry,
    ) -> None:
        """Store a response in cache."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all cached entries."""
        pass

class MemoryCache(BaseCache):
    """Simple in-memory cache implementation."""
    
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
    
    def get(self, key: str) -> Optional[CacheEntry]:
        if key not in self._cache:
            return None
            
        entry = self._cache[key]
        if entry.is_expired():
            del self._cache[key]
            return None
            
        return entry
    
    def set(
        self, 
        key: str, 
        entry: CacheEntry,
    ) -> None:
        self._cache[key] = entry
    
    def clear(self) -> None:
        self._cache.clear()

def generate_cache_key(
    messages: list,
    model: str,
    temperature: float,
    **kwargs
) -> str:
    """Generate a unique cache key for a request."""
    # Create a dictionary with all parameters that affect the response
    key_data = {
        "messages": messages,
        "model": model,
        "temperature": temperature,
        **kwargs
    }
    
    # Convert to a stable string representation
    key_str = json.dumps(key_data, sort_keys=True)
    
    # Generate hash
    return hashlib.sha256(key_str.encode()).hexdigest() 