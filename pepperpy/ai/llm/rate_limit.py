"""Rate limiting implementation for LLM APIs."""
from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import asyncio
import time

@dataclass
class RateLimit:
    """Configuration for rate limiting."""
    requests_per_minute: int
    requests_per_hour: Optional[int] = None
    concurrent_requests: Optional[int] = None

@dataclass
class RateLimitState:
    """Tracks current rate limit state."""
    minute_requests: int = 0
    hour_requests: int = 0
    last_minute_reset: datetime = field(default_factory=datetime.now)
    last_hour_reset: datetime = field(default_factory=datetime.now)
    semaphore: asyncio.Semaphore = field(default_factory=lambda: asyncio.Semaphore(10))

class RateLimiter:
    """Manages rate limiting for API calls."""
    
    def __init__(self, config: RateLimit):
        self.config = config
        self.state = RateLimitState()
        if config.concurrent_requests:
            self.state.semaphore = asyncio.Semaphore(config.concurrent_requests)
    
    async def acquire(self):
        """Acquire permission to make a request."""
        await self._reset_counters()
        await self._wait_if_needed()
        
        async with self.state.semaphore:
            self.state.minute_requests += 1
            self.state.hour_requests += 1
            
    async def _reset_counters(self):
        """Reset counters if time windows have passed."""
        now = datetime.now()
        
        # Reset minute counter
        if now - self.state.last_minute_reset >= timedelta(minutes=1):
            self.state.minute_requests = 0
            self.state.last_minute_reset = now
        
        # Reset hour counter
        if now - self.state.last_hour_reset >= timedelta(hours=1):
            self.state.hour_requests = 0
            self.state.last_hour_reset = now
    
    async def _wait_if_needed(self):
        """Wait if we're at the rate limit."""
        while True:
            if self.state.minute_requests >= self.config.requests_per_minute:
                # Wait until next minute
                wait_time = 60 - (datetime.now() - self.state.last_minute_reset).seconds
                await asyncio.sleep(wait_time)
                continue
            
            if (self.config.requests_per_hour and 
                self.state.hour_requests >= self.config.requests_per_hour):
                # Wait until next hour
                wait_time = 3600 - (datetime.now() - self.state.last_hour_reset).seconds
                await asyncio.sleep(wait_time)
                continue
            
            break 