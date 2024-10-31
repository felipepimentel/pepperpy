"""Telemetry and metrics collection."""
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import time
import threading
from contextlib import contextmanager

@dataclass
class MetricPoint:
    """Single metric measurement."""
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)

class MetricsCollector:
    """Collect and aggregate metrics."""
    
    def __init__(self):
        self._metrics: Dict[str, list[MetricPoint]] = {}
        self._lock = threading.Lock()
        
    def record(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None
    ):
        """Record a metric value."""
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = []
            self._metrics[name].append(
                MetricPoint(value, datetime.now(), labels or {})
            )
            
    @contextmanager
    def timer(self, name: str, labels: Optional[Dict[str, str]] = None):
        """Time a block of code."""
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start
            self.record(name, duration, labels)
            
    def get_metrics(self) -> Dict[str, Any]:
        """Get all recorded metrics."""
        with self._lock:
            return {
                name: [
                    {
                        "value": point.value,
                        "timestamp": point.timestamp.isoformat(),
                        "labels": point.labels
                    }
                    for point in points
                ]
                for name, points in self._metrics.items()
            }
            
    def clear(self):
        """Clear all recorded metrics."""
        with self._lock:
            self._metrics.clear()

# Global metrics collector
metrics = MetricsCollector() 