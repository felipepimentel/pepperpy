"""Core metrics module"""

from abc import ABC, abstractmethod

from .collectors import MetricsCollector
from .exceptions import MetricsError
from .types import Metric, MetricType, MetricValue


class MetricsProvider(ABC):
    """Base metrics provider interface"""

    @abstractmethod
    async def record(self, metric: Metric) -> None:
        """Record a metric"""
        pass

    @abstractmethod
    async def increment(self, name: str, value: int = 1, **tags: str) -> None:
        """Increment counter metric"""
        pass

    @abstractmethod
    async def gauge(self, name: str, value: float, **tags: str) -> None:
        """Record gauge metric"""
        pass

    @abstractmethod
    async def histogram(self, name: str, value: float, **tags: str) -> None:
        """Record histogram metric"""
        pass


__all__ = [
    "MetricsProvider",
    "MetricsCollector",
    "MetricsError",
    "Metric",
    "MetricType",
    "MetricValue",
]
