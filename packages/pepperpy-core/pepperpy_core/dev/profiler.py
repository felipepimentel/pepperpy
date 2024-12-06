"""Profiling utilities for performance analysis."""

import cProfile
import io
import logging
import pstats
from collections.abc import Callable, Generator
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import Any, TextIO, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def profile_to_file(
    output_file: str | Path, sort_by: str = "cumulative"
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to profile a function and save results to a file.

    Args:
        output_file: Path to save profiling results
        sort_by: Stats sorting key (default: cumulative)

    Returns:
        Decorated function
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            profiler = cProfile.Profile()
            try:
                result = profiler.runcall(func, *args, **kwargs)
                stats = pstats.Stats(profiler)
                stats.sort_stats(sort_by)

                # Ensure directory exists
                if isinstance(output_file, str | Path):
                    path = Path(output_file)
                else:
                    path = output_file
                path.parent.mkdir(parents=True, exist_ok=True)

                # Save stats
                stats.dump_stats(str(path))
                return result
            finally:
                profiler.disable()

        return wrapper

    return decorator


@contextmanager
def profile_section(
    output: str | Path | TextIO, sort_by: str = "cumulative"
) -> Generator[None, None, None]:
    """Context manager for profiling a code section.

    Args:
        output: Where to write profiling results (file path or file-like object)
        sort_by: Stats sorting key (default: cumulative)
    """
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        yield
    finally:
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats(sort_by)

        if isinstance(output, str | Path):
            # Ensure directory exists for file path
            path = Path(output)
            path.parent.mkdir(parents=True, exist_ok=True)
            stats.dump_stats(str(path))
        else:
            # Write to file-like object
            stream = io.StringIO()
            stats.print_stats()
            output.write(stream.getvalue())
