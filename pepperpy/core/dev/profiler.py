"""Profiling utilities"""

import asyncio
import cProfile
import functools
import pstats
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Callable, Dict, Optional, TypeVar

from pepperpy.core.logging import get_logger

T = TypeVar("T")


class AsyncProfiler:
    """Async function profiler"""

    def __init__(self, name: str):
        self.name = name
        self._profiler = cProfile.Profile()
        self._logger = get_logger(__name__)
        self._stats: Dict[str, pstats.Stats] = {}

    @asynccontextmanager
    async def profile(self) -> AsyncIterator["AsyncProfiler"]:
        """Profile execution with detailed statistics

        Returns:
            AsyncIterator[AsyncProfiler]: Profiler instance
        """
        self._profiler.enable()
        try:
            yield self
        finally:
            self._profiler.disable()
            stats = pstats.Stats(self._profiler)
            stats.sort_stats("cumulative")
            self._stats[self.name] = stats
            await self._logger.debug(
                f"Profile stats for {self.name}",
                total_calls=stats.total_calls,
                total_time=stats.total_tt,
            )

    def profile_function(self, func: Callable[..., T]) -> Callable[..., T]:
        """Decorator for profiling async functions

        Args:
            func: Function to profile

        Returns:
            Callable[..., T]: Decorated function
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Can only profile async functions")

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            profiler = AsyncProfiler(f"{func.__name__}_{id(func)}")
            async with profiler.profile():
                return await func(*args, **kwargs)

        return wrapper

    def print_stats(self, limit: Optional[int] = None) -> None:
        """Print profiling statistics"""
        for name, stats in self._stats.items():
            print(f"\nProfile stats for {name}:")
            stats.print_stats(limit)

    def get_stats(self) -> Dict[str, pstats.Stats]:
        """Get raw profiling statistics"""
        return self._stats
