"""Metrics collection utilities"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable

from pepperpy.core.exceptions import PepperPyError


class MetricsError(PepperPyError):
    """Metrics collection error"""


MetricValue = Union[int, float, str]


@runtime_checkable
class Metric(Protocol):
    """Metric protocol"""

    name: str
    description: str
    value: MetricValue
    labels: Dict[str, str]


@dataclass
class MetricData:
    """Metric data"""

    name: str
    value: MetricValue
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MetricsCollector:
    """System metrics collector"""

    def __init__(self):
        self._metrics: Dict[str, List[MetricData]] = {}

    def record(
        self,
        name: str,
        value: MetricValue,
        labels: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record metric value

        Args:
            name: Metric name
            value: Metric value
            labels: Optional metric labels
            metadata: Optional metric metadata
        """
        metric = MetricData(
            name=name,
            value=value,
            labels=labels or {},
            metadata=metadata or {},
        )

        if name not in self._metrics:
            self._metrics[name] = []
        self._metrics[name].append(metric)

    def get_metrics(self, name: Optional[str] = None) -> Dict[str, List[MetricData]]:
        """Get recorded metrics

        Args:
            name: Optional name of specific metric to get

        Returns:
            Dict[str, List[MetricData]]: Recorded metrics
        """
        if name:
            if name not in self._metrics:
                raise MetricsError(f"Metric not found: {name}")
            return {name: self._metrics[name]}
        return self._metrics.copy()

    def clear(self, name: Optional[str] = None) -> None:
        """Clear recorded metrics

        Args:
            name: Optional name of specific metric to clear
        """
        if name:
            if name in self._metrics:
                del self._metrics[name]
        else:
            self._metrics.clear()


# Global metrics collector instance
collector = MetricsCollector()
