"""Benchmark utilities."""

import time
from dataclasses import dataclass, field
from typing import Any

from ..logging import BaseLogger
from ..types import JsonDict


@dataclass
class BenchmarkResult:
    """Benchmark result."""

    name: str
    duration: float
    iterations: int
    metadata: JsonDict = field(default_factory=dict)

    @property
    def avg_duration(self) -> float:
        """Get average duration per iteration."""
        return self.duration / self.iterations if self.iterations > 0 else 0.0


class Benchmark:
    """Benchmark utility."""

    def __init__(
        self,
        name: str,
        logger: BaseLogger | None = None,
        metadata: JsonDict | None = None,
    ) -> None:
        """Initialize benchmark.

        Args:
            name: Benchmark name
            logger: Optional logger
            metadata: Optional metadata
        """
        self.name = name
        self.logger = logger
        self.metadata = metadata or {}
        self._start_time: float | None = None
        self._iterations = 0

    def __enter__(self) -> "Benchmark":
        """Start benchmark."""
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, *args: Any) -> None:
        """End benchmark."""
        if not self._start_time:
            return

        duration = time.perf_counter() - self._start_time
        result = BenchmarkResult(
            name=self.name,
            duration=duration,
            iterations=self._iterations,
            metadata=self.metadata,
        )

        if self.logger:
            self.logger.info(
                f"Benchmark {self.name}: {result.avg_duration:.6f}s per iteration",
                benchmark=result.__dict__,
            )

    def iteration(self) -> None:
        """Record iteration."""
        self._iterations += 1
