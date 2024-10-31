"""Distributed caching system with multiple backends."""
from typing import Any, Optional, Union
from datetime import timedelta
import pickle
import redis
import memcache
from pydantic import BaseModel

class CacheConfig(BaseModel):
    """Cache configuration."""
    backend: str = "redis"
    url: str = "redis://localhost:6379/0"
    prefix: str = "pepperpy:"
    default_ttl: int = 3600

class DistributedCache:
    """Distributed cache implementation."""
    
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        
        if self.config.backend == "redis":
            self.client = redis.from_url(self.config.url)
        elif self.config.backend == "memcached":
            host, port = self.config.url.split(":")
            self.client = memcache.Client([f"{host}:{port}"])
        else:
            raise ValueError(f"Unsupported cache backend: {self.config.backend}")
    
    def _make_key(self, key: str) -> str:
        """Create prefixed cache key."""
        return f"{self.config.prefix}{key}"
    
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache."""
        value = self.client.get(self._make_key(key))
        return pickle.loads(value) if value else default
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[Union[int, timedelta]] = None
    ) -> None:
        """Set value in cache."""
        if isinstance(ttl, timedelta):
            ttl = int(ttl.total_seconds())
        
        serialized = pickle.dumps(value)
        self.client.set(
            self._make_key(key),
            serialized,
            ttl or self.config.default_ttl
        ) 