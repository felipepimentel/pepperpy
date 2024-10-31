"""Telemetry collection system."""
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import time
import psutil
import platform
from ..core.config import Config

@dataclass
class SystemMetrics:
    """System metrics container."""
    cpu_percent: float
    memory_percent: float
    disk_usage: Dict[str, float]
    network_io: Dict[str, int]
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ApplicationMetrics:
    """Application metrics container."""
    active_connections: int
    requests_per_second: float
    average_response_time: float
    error_rate: float
    timestamp: datetime = field(default_factory=datetime.now)

class TelemetryCollector:
    """Collect and manage telemetry data."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._system_metrics: List[SystemMetrics] = []
        self._app_metrics: List[ApplicationMetrics] = []
        self._max_history = int(self.config.get("TELEMETRY_HISTORY", 1000))
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect system metrics."""
        metrics = SystemMetrics(
            cpu_percent=psutil.cpu_percent(),
            memory_percent=psutil.virtual_memory().percent,
            disk_usage={
                disk.mountpoint: disk.percent
                for disk in psutil.disk_partitions()
                if disk.fstype
            },
            network_io={
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        )
        
        self._system_metrics.append(metrics)
        if len(self._system_metrics) > self._max_history:
            self._system_metrics.pop(0)
        
        return metrics
    
    def collect_app_metrics(
        self,
        connections: int,
        requests: float,
        response_time: float,
        errors: float
    ) -> ApplicationMetrics:
        """Collect application metrics."""
        metrics = ApplicationMetrics(
            active_connections=connections,
            requests_per_second=requests,
            average_response_time=response_time,
            error_rate=errors
        )
        
        self._app_metrics.append(metrics)
        if len(self._app_metrics) > self._max_history:
            self._app_metrics.pop(0)
        
        return metrics
    
    def get_system_metrics(
        self,
        limit: Optional[int] = None
    ) -> List[SystemMetrics]:
        """Get collected system metrics."""
        metrics = self._system_metrics
        if limit:
            metrics = metrics[-limit:]
        return metrics
    
    def get_app_metrics(
        self,
        limit: Optional[int] = None
    ) -> List[ApplicationMetrics]:
        """Get collected application metrics."""
        metrics = self._app_metrics
        if limit:
            metrics = metrics[-limit:]
        return metrics 