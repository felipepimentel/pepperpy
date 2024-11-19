"""Benchmark utilities"""

import time
from dataclasses import dataclass
from typing import Any, Callable

from pepperpy.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class BenchmarkConfig:
    """Benchmark configuration"""

    iterations: int = 1000
    warmup: int = 100
    debug: bool = False


@dataclass
class BenchmarkResult:
    """Benchmark result"""

    name: str
    iterations: int
    total_time: float
    avg_time: float
    min_time: float
    max_time: float
    metadata: dict[str, Any]


async def benchmark(
    func: Callable[..., Any],
    *args: Any,
    config: BenchmarkConfig | None = None,
    **kwargs: Any,
) -> BenchmarkResult:
    """Run benchmark on function"""
    config = config or BenchmarkConfig()

    try:
        # Warmup
        for _ in range(config.warmup):
            await func(*args, **kwargs)

        # Benchmark
        times: list[float] = []
        for _ in range(config.iterations):
            start = time.perf_counter()
            await func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)

        total_time = sum(times)
        avg_time = total_time / len(times)
        min_time = min(times)
        max_time = max(times)

        result = BenchmarkResult(
            name=func.__name__,
            iterations=config.iterations,
            total_time=total_time,
            avg_time=avg_time,
            min_time=min_time,
            max_time=max_time,
            metadata={
                "warmup": config.warmup,
                "debug": config.debug,
            },
        )

        if config.debug:
            await logger.debug(
                f"Benchmark {func.__name__} completed",
                result=result.__dict__,
            )

        return result

    except Exception as e:
        await logger.error(
            f"Benchmark {func.__name__} failed",
            error=str(e),
        )
        raise
