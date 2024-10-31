"""Metrics collection and monitoring system."""
from typing import Dict, List, Optional
from datetime import datetime
import time
from dataclasses import dataclass, field
import prometheus_client as prom
from pydantic import BaseModel

class MetricsConfig(BaseModel):
    """Metrics configuration."""
    enabled: bool = True
    prometheus_port: int = 9090
    collect_interval: int = 60

@dataclass
class MetricPoint:
    """Single metric measurement."""
    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)

class MetricsCollector:
    """Collect and expose metrics."""
    
    def __init__(self, config: Optional[MetricsConfig] = None):
        self.config = config or MetricsConfig()
        
        # Prometheus metrics
        self.request_latency = prom.Histogram(
            'request_duration_seconds',
            'Request latency in seconds',
            ['method', 'endpoint']
        )
        
        self.error_counter = prom.Counter(
            'errors_total',
            'Total number of errors',
            ['type']
        )
        
        if self.config.enabled:
            prom.start_http_server(self.config.prometheus_port)
    
    def measure_time(self, name: str, labels: Optional[Dict[str, str]] = None):
        """Context manager for timing operations."""
        start = time.time()
        labels = labels or {}
        
        def _complete():
            duration = time.time() - start
            self.request_latency.labels(
                method=labels.get('method', ''),
                endpoint=labels.get('endpoint', '')
            ).observe(duration)
        
        return _complete
    
    def count_error(self, error_type: str):
        """Increment error counter."""
        self.error_counter.labels(type=error_type).inc() 