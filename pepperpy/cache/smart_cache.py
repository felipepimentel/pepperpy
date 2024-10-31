"""Smart caching system with automatic invalidation."""
from typing import Any, Optional, Union
from datetime import datetime, timedelta
import hashlib
import json
import asyncio
from functools import wraps

class SmartCache:
    def __init__(self, backend: str = "memory", ttl: int = 300):
        self._cache = {}
        self._metadata = {}
        self._backend = backend
        self._default_ttl = ttl
    
    def _get_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_data = {
            'args': args,
            'kwargs': kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def cached(self, ttl: Optional[int] = None, 
              condition: Optional[callable] = None):
        """Smart caching decorator."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                if condition and not condition(*args, **kwargs):
                    return await func(*args, **kwargs)
                
                cache_key = self._get_key(func.__name__, *args, **kwargs)
                
                # Check cache
                if self._is_valid(cache_key):
                    self._metadata[cache_key]['hits'] += 1
                    return self._cache[cache_key]
                
                # Execute function
                result = await func(*args, **kwargs)
                
                # Cache result
                self._cache[cache_key] = result
                self._metadata[cache_key] = {
                    'created_at': datetime.now(),
                    'ttl': ttl or self._default_ttl,
                    'hits': 1
                }
                
                return result
            return wrapper
        return decorator
    
    def _is_valid(self, key: str) -> bool:
        """Check if cache entry is valid."""
        if key not in self._cache or key not in self._metadata:
            return False
            
        metadata = self._metadata[key]
        age = datetime.now() - metadata['created_at']
        
        return age.total_seconds() < metadata['ttl']
    
    async def invalidate(self, pattern: Optional[str] = None):
        """Invalidate cache entries."""
        if pattern:
            keys = [k for k in self._cache.keys() if pattern in k]
        else:
            keys = list(self._cache.keys())
            
        for key in keys:
            del self._cache[key]
            del self._metadata[key] 