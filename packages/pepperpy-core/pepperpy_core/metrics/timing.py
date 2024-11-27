"""Timing decorator implementation"""

from functools import wraps
from typing import Any, Callable, Coroutine, Dict, Optional, TypeVar

from ..utils.datetime import utc_now
from .base import MetricsCollector

F = TypeVar("F", bound=Callable[..., Coroutine[Any, Any, Any]])


def timing(name: str, labels: Optional[Dict[str, str]] = None) -> Callable[[F], F]:
    """Timing decorator for async functions

    Args:
        name: Metric name
        labels: Optional metric labels

    Returns:
        Decorator function
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = utc_now()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = (utc_now() - start).total_seconds()
                if args and hasattr(args[0], "metrics"):
                    collector = args[0].metrics
                    if isinstance(collector, MetricsCollector):
                        collector.histogram(f"{name}_duration_seconds", duration, labels=labels)

        return wrapper  # type: ignore

    return decorator


__all__ = [
    "timing",
]
