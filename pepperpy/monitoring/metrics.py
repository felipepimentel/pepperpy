"""Metrics collection and monitoring system."""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import time
import psutil
from ..core.context import ExecutionContext

@dataclass
class OperationMetrics:
    """Metrics for a single operation."""
    operation_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    success: bool = True
    error: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

class MetricsCollector:
    """Collect and manage metrics."""
    
    def __init__(self):
        self._operations: Dict[str, OperationMetrics] = {}
        self._system_metrics = SystemMetricsCollector()
    
    def start_operation(
        self,
        operation_id: str,
        context: Optional[ExecutionContext] = None
    ) -> None:
        """Start tracking an operation."""
        self._operations[operation_id] = OperationMetrics(
            operation_id=operation_id,
            start_time=datetime.now(),
            context=context.metadata if context else {}
        )
    
    def end_operation(
        self,
        operation_id: str,
        success: bool = True,
        error: Optional[str] = None
    ) -> None:
        """End tracking an operation."""
        if operation := self._operations.get(operation_id):
            operation.end_time = datetime.now()
            operation.duration_ms = (
                operation.end_time - operation.start_time
            ).total_seconds() * 1000
            operation.success = success
            operation.error = error
    
    def get_metrics(
        self,
        operation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get collected metrics."""
        metrics = {
            "operations": {},
            "system": self._system_metrics.get_current()
        }
        
        if operation_id:
            if operation := self._operations.get(operation_id):
                metrics["operations"][operation_id] = operation
        else:
            metrics["operations"] = self._operations
        
        return metrics

class SystemMetricsCollector:
    """Collect system metrics."""
    
    def get_current(self) -> Dict[str, float]:
        """Get current system metrics."""
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        } 