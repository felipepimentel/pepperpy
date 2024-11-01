from functools import wraps
from typing import Callable, Any
import asyncio
from ..cache import Cache

def cached(ttl: int = 300):
    """Cache function results."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            if result := await cache.get(cache_key):
                return result
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator

def retry(attempts: int = 3, delay: float = 1.0):
    """Retry failed operations."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            for attempt in range(attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == attempts - 1:
                        raise
                    await asyncio.sleep(delay)
        return wrapper
    return decorator 