"""Benchmarking utilities"""

import asyncio
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator, Callable, Dict, List, Optional

from pepperpy.core.logging import get_logger


@dataclass
class BenchmarkResult:
    """Benchmark measurement result"""

    name: str
    duration: float
    iterations: int
    metadata: Dict[str, Any]
    stats: Dict[str, float]


class AsyncBenchmark:
    """Async function benchmarking"""

    def __init__(self, name: str):
        self.name = name
        self._results: List[float] = []
        self._metadata: Dict[str, Any] = {}
        self._logger = get_logger(__name__)

    @asynccontextmanager
    async def measure(self) -> AsyncIterator[BenchmarkResult]:
        """Measure execution time

        Returns:
            AsyncIterator[BenchmarkResult]: Benchmark measurement result
        """
        start_time = time.perf_counter()
        try:
            yield None
        finally:
            duration = time.perf_counter() - start_time
            self._results.append(duration)
            await self._logger.debug(
                f"Benchmark {self.name}: {duration:.6f}s", duration=duration, **self._metadata
            )

    async def run(
        self,
        func: Callable,
        iterations: int = 1,
        warmup: int = 0,
        cooldown: float = 0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> BenchmarkResult:
        """Run benchmark

        Args:
            func: Function to benchmark
            iterations: Number of iterations
            warmup: Number of warmup iterations
            cooldown: Cooldown time between iterations
            metadata: Additional metadata

        Returns:
            BenchmarkResult: Benchmark results
        """
        self._metadata = metadata or {}

        # Warmup
        for _ in range(warmup):
            await func()
            if cooldown > 0:
                await asyncio.sleep(cooldown)

        # Benchmark
        for _ in range(iterations):
            async with self.measure():
                await func()
            if cooldown > 0:
                await asyncio.sleep(cooldown)

        # Calculate stats
        durations = self._results[-iterations:]
        stats = {
            "min": min(durations),
            "max": max(durations),
            "avg": sum(durations) / len(durations),
            "total": sum(durations),
        }

        return BenchmarkResult(
            name=self.name,
            duration=stats["total"],
            iterations=iterations,
            metadata=self._metadata,
            stats=stats,
        )
