"""Rate limiting implementation."""
from typing import Optional, Dict
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass
import time

@dataclass
class RateLimit:
    """Rate limit configuration."""
    calls: int
    period: int  # seconds
    retry_after: Optional[int] = None

class RateLimiter:
    """Token bucket rate limiter implementation."""
    
    def __init__(self, limit: RateLimit):
        self.limit = limit
        self.tokens = limit.calls
        self.last_update = time.time()
        self._locks: Dict[str, asyncio.Lock] = {}
    
    def _get_lock(self, key: str) -> asyncio.Lock:
        """Get or create lock for key."""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]
    
    async def acquire(self, key: str = "default") -> bool:
        """Acquire rate limit token."""
        async with self._get_lock(key):
            now = time.time()
            time_passed = now - self.last_update
            self.last_update = now
            
            # Replenish tokens
            self.tokens = min(
                self.limit.calls,
                self.tokens + time_passed * (self.limit.calls / self.limit.period)
            )
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            
            if self.limit.retry_after:
                await asyncio.sleep(self.limit.retry_after)
                return await self.acquire(key)
            
            return False
    
    def reset(self, key: str = "default"):
        """Reset rate limit for key."""
        self.tokens = self.limit.calls
        self.last_update = time.time() 