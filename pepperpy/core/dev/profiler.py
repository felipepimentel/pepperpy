"""Profiling utilities"""

import cProfile
import io
import pstats
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager, redirect_stdout
from dataclasses import dataclass
from typing import Any, TypeVar

from pepperpy.core.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


@dataclass
class ProfilerConfig:
    """Profiler configuration"""

    sort_by: str = "cumulative"
    lines: int = 20
    debug: bool = False


@asynccontextmanager
async def profile(
    name: str,
    config: ProfilerConfig | None = None,
) -> AsyncIterator[cProfile.Profile]:
    """Profile code block"""
    config = config or ProfilerConfig()
    profiler = cProfile.Profile()

    try:
        profiler.enable()
        yield profiler

    finally:
        profiler.disable()
        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s)
        stats.sort_stats(config.sort_by)

        with redirect_stdout(s):
            stats.print_stats(config.lines)

        if config.debug:
            await logger.debug(
                f"Profile {name} completed",
                output=s.getvalue(),
            )


async def profile_func(
    func: Callable[..., Awaitable[T]],
    *args: Any,
    config: ProfilerConfig | None = None,
    **kwargs: Any,
) -> T:
    """Profile async function"""
    async with profile(func.__name__, config) as _:
        return await func(*args, **kwargs)
