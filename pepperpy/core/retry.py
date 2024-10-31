"""Retry mechanism with exponential backoff."""
from typing import TypeVar, Callable, Optional, Type, Union
from dataclasses import dataclass
import asyncio
import random
from functools import wraps

T = TypeVar('T')

@dataclass
class RetryConfig:
    """Retry configuration."""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    retry_exceptions: tuple[Type[Exception], ...] = (Exception,)

def retry_async(config: Optional[RetryConfig] = None):
    """Decorator for async functions with retry logic."""
    config = config or RetryConfig()
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            attempt = 0
            last_exception = None
            
            while attempt < config.max_attempts:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if not isinstance(e, config.retry_exceptions):
                        raise
                    
                    attempt += 1
                    last_exception = e
                    
                    if attempt == config.max_attempts:
                        break
                    
                    # Calculate delay with exponential backoff
                    delay = min(
                        config.initial_delay * (config.exponential_base ** attempt),
                        config.max_delay
                    )
                    
                    # Add jitter if configured
                    if config.jitter:
                        delay *= (0.5 + random.random())
                    
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        return wrapper
    
    return decorator 