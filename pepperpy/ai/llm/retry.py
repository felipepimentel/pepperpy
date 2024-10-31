"""Retry mechanism for LLM API calls."""
from typing import Type, Callable, TypeVar, Optional
import asyncio
from functools import wraps
import random

T = TypeVar('T')

class RetryConfig:
    """Configuration for retry behavior."""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        exponential_base: float = 2.0,
        jitter: bool = True
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for a given attempt."""
        delay = min(
            self.base_delay * (self.exponential_base ** attempt),
            self.max_delay
        )
        
        if self.jitter:
            delay *= random.uniform(0.5, 1.5)
            
        return delay

def retry_async(
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    config: Optional[RetryConfig] = None,
    should_retry: Optional[Callable[[Exception], bool]] = None
):
    """Decorator for async functions that need retry logic."""
    config = config or RetryConfig()
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == config.max_retries:
                        raise
                        
                    if should_retry and not should_retry(e):
                        raise
                        
                    delay = config.calculate_delay(attempt)
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        return wrapper
    
    return decorator 