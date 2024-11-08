"""Core metrics collection and monitoring system"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Protocol

from .base import BaseModule, ModuleConfig
from .exceptions import MetricError
from .types import JsonDict


class MetricType(Enum):
    """Types of metrics supported"""

    COUNTER = auto()
    GAUGE = auto()
    HISTOGRAM = auto()
    SUMMARY = auto()


@dataclass
class MetricConfig(ModuleConfig):
    """Metrics module configuration"""

    enable_persistence: bool = False
    flush_interval: float = 60.0  # seconds
    max_buffer_size: int = 1000
    default_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class Metric:
    """Enhanced metric data structure"""

    name: str
    value: Any
    type: MetricType
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)
    module: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self) -> JsonDict:
        """Convert metric to dictionary"""
        return {
            "name": self.name,
            "value": self.value,
            "type": self.type.name,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels,
            "module": self.module,
            "description": self.description,
        }


class MetricsProtocol(Protocol):
    """Protocol for metrics storage backends"""

    async def store(self, metric: Metric) -> None: ...
    async def retrieve(
        self, name: str, start: Optional[datetime] = None, end: Optional[datetime] = None
    ) -> List[Metric]: ...
    async def flush(self) -> None: ...


class MetricsModule(BaseModule):
    """Enhanced metrics management system"""

    __module_name__ = "metrics"
    __dependencies__ = ["storage"]

    def __init__(self, config: Optional[MetricConfig] = None):
        super().__init__(config or MetricConfig())
        self._metrics: Dict[str, Dict[str, Metric]] = {}
        self._buffer: List[Metric] = []
        self._lock = asyncio.Lock()
        self._flush_task: Optional[asyncio.Task] = None

    async def initialize(self) -> None:
        """Initialize metrics system"""
        await super().initialize()
        if self.config.enable_persistence:
            self._flush_task = asyncio.create_task(self._periodic_flush())

    async def cleanup(self) -> None:
        """Cleanup metrics system"""
        if self._flush_task:
            self._flush_task.cancel()
            try:
                await self._flush_task
            except asyncio.CancelledError:
                pass

        if self._buffer:
            await self._flush_metrics()

        self._metrics.clear()
        self._buffer.clear()
        await super().cleanup()

    async def record(self, metric: Metric, flush: bool = False) -> None:
        """
        Record a new metric value

        Args:
            metric: Metric to record
            flush: Whether to flush metrics immediately

        Raises:
            MetricError: If metric recording fails
        """
        try:
            async with self._lock:
                if metric.module not in self._metrics:
                    self._metrics[metric.module] = {}

                self._metrics[metric.module][metric.name] = metric

                if self.config.enable_persistence:
                    self._buffer.append(metric)

                    if flush or len(self._buffer) >= self.config.max_buffer_size:
                        await self._flush_metrics()

        except Exception as e:
            raise MetricError(f"Failed to record metric: {e}") from e

    async def get_metric(self, module: str, name: str) -> Optional[Metric]:
        """Get specific metric value"""
        return self._metrics.get(module, {}).get(name)

    async def get_module_metrics(self, module: str) -> Dict[str, Metric]:
        """Get all metrics for a module"""
        return self._metrics.get(module, {}).copy()

    async def _periodic_flush(self) -> None:
        """Periodically flush metrics to storage"""
        while True:
            try:
                await asyncio.sleep(self.config.flush_interval)
                if self._buffer:
                    await self._flush_metrics()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._logger.error(f"Error in periodic flush: {e}")

    async def _flush_metrics(self) -> None:
        """Flush buffered metrics to storage"""
        if not self._buffer:
            return

        try:
            storage = self.get_module("storage")
            if storage:
                metrics_data = [m.to_dict() for m in self._buffer]
                await storage.save_json("metrics.json", metrics_data)
                self._buffer.clear()
        except Exception as e:
            self._logger.error(f"Failed to flush metrics: {e}")
