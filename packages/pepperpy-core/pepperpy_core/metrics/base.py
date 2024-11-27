"""Base metrics implementation"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Callable, Dict, Optional

from ..base.types import JsonDict
from ..utils.datetime import utc_now


class MetricType(str, Enum):
    """Metric types"""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class Metric:
    """Metric data"""

    name: str
    type: MetricType
    value: float
    timestamp: datetime = field(default_factory=utc_now)
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class MetricsConfig:
    """Metrics configuration"""

    enabled: bool = True
    prefix: str = ""
    default_labels: Dict[str, str] = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)


class MetricsCollector:
    """Metrics collector implementation"""

    def __init__(self, config: Optional[MetricsConfig] = None) -> None:
        self.config = config or MetricsConfig()
        self._metrics: Dict[str, list[Metric]] = {}
        self._collectors: Dict[str, Callable[[], list[Metric]]] = {}

    def _add_prefix(self, name: str) -> str:
        """Add prefix to metric name"""
        if not self.config.prefix:
            return name
        if name.startswith(self.config.prefix):
            return name
        return f"{self.config.prefix}{name}"

    def counter(
        self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Record counter metric"""
        if not self.config.enabled:
            return
        self._record(name, MetricType.COUNTER, value, labels)

    def gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record gauge metric"""
        if not self.config.enabled:
            return
        self._record(name, MetricType.GAUGE, value, labels)

    def histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record histogram metric"""
        if not self.config.enabled:
            return
        self._record(name, MetricType.HISTOGRAM, value, labels)

    def summary(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Record summary metric"""
        if not self.config.enabled:
            return
        self._record(name, MetricType.SUMMARY, value, labels)

    def register_collector(self, name: str, collector: Callable[[], list[Metric]]) -> None:
        """Register metrics collector"""

        def wrapped_collector() -> list[Metric]:
            metrics = collector()
            for metric in metrics:
                metric.name = self._add_prefix(metric.name)
            return metrics

        self._collectors[name] = wrapped_collector

    def _record(
        self, name: str, type: MetricType, value: float, labels: Optional[Dict[str, str]] = None
    ) -> None:
        """Record metric"""
        metric = Metric(
            name=self._add_prefix(name),
            type=type,
            value=value,
            labels={**self.config.default_labels, **(labels or {})},
            timestamp=utc_now(),
        )
        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(metric)

    def collect(self) -> list[Metric]:
        """Collect all metrics"""
        metrics = []

        # Collect stored metrics
        for metric_list in self._metrics.values():
            metrics.extend(metric_list)

        # Run collectors
        for collector in self._collectors.values():
            metrics.extend(collector())

        return metrics

    def clear(self) -> None:
        """Clear all metrics"""
        self._metrics.clear()


__all__ = [
    "Metric",
    "MetricsConfig",
    "MetricsCollector",
    "MetricType",
]
