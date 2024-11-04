from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

from .health import HealthStatus


@dataclass
class HealthCheck:
    """Health check result"""

    status: HealthStatus
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    details: Optional[Dict[str, Any]] = None


class HealthMonitor:
    """Module health monitoring"""

    def __init__(self) -> None:
        self._checks: Dict[str, HealthCheck] = {}

    def update(self, module_name: str, check: HealthCheck) -> None:
        """Update module health status"""
        self._checks[module_name] = check

    def get_status(self, module_name: str) -> Optional[HealthCheck]:
        """Get module health status"""
        return self._checks.get(module_name)

    def get_all(self) -> Dict[str, HealthCheck]:
        """Get all health checks"""
        return dict(self._checks)
