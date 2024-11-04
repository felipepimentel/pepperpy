from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from .types import JsonDict


class HealthStatus(str, Enum):
    """Status de saúde do sistema"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    STARTING = "starting"
    STOPPING = "stopping"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Resultado de verificação de saúde"""

    status: HealthStatus
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    details: Optional[JsonDict] = None
    checks: Dict[str, "HealthCheck"] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "status": self.status,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details or {},
            "checks": {k: v.to_dict() for k, v in self.checks.items()},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HealthCheck":
        """Cria a partir de dicionário"""
        return cls(
            status=HealthStatus(data["status"]),
            message=data["message"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            details=data.get("details"),
            checks={k: cls.from_dict(v) for k, v in data.get("checks", {}).items()},
        )


class HealthMonitor:
    """Monitor de saúde do sistema"""

    def __init__(self):
        self._checks: Dict[str, HealthCheck] = {}
        self._status = HealthStatus.STARTING
        self._listeners: List[callable] = []

    @property
    def status(self) -> HealthStatus:
        """Status geral do sistema"""
        if not self._checks:
            return self._status

        if any(
            check.status == HealthStatus.UNHEALTHY for check in self._checks.values()
        ):
            return HealthStatus.UNHEALTHY

        if any(
            check.status == HealthStatus.DEGRADED for check in self._checks.values()
        ):
            return HealthStatus.DEGRADED

        return HealthStatus.HEALTHY

    def add_listener(self, listener: callable) -> None:
        """Adiciona listener para mudanças de status"""
        self._listeners.append(listener)

    def update(self, component: str, check: HealthCheck) -> None:
        """Atualiza status de um componente"""
        previous = self._checks.get(component)
        self._checks[component] = check

        if previous and previous.status != check.status:
            self._notify_status_change(component, previous.status, check.status)

    def get_check(self, component: str) -> Optional[HealthCheck]:
        """Obtém status de um componente"""
        return self._checks.get(component)

    def get_all_checks(self) -> Dict[str, HealthCheck]:
        """Obtém todos os status"""
        return dict(self._checks)

    def get_system_health(self) -> HealthCheck:
        """Obtém saúde geral do sistema"""
        return HealthCheck(
            status=self.status, message=f"System is {self.status}", checks=self._checks
        )

    def _notify_status_change(
        self, component: str, old_status: HealthStatus, new_status: HealthStatus
    ) -> None:
        """Notifica mudanças de status"""
        for listener in self._listeners:
            try:
                listener(component, old_status, new_status)
            except Exception as e:
                print(f"Error in health listener: {str(e)}")

    def clear(self) -> None:
        """Limpa todos os checks"""
        self._checks.clear()
        self._status = HealthStatus.UNKNOWN
