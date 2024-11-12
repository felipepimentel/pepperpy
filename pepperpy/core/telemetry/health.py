"""Health check implementation"""

import asyncio
from datetime import datetime
from enum import Enum
from typing import Any, Dict


class HealthStatus(Enum):
    """Health check status"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheck:
    """Health check manager"""

    def __init__(self, interval: int = 60):
        self._checks: Dict[str, callable] = {}
        self._results: Dict[str, Dict[str, Any]] = {}
        self._interval = interval
        self._task = None
        self._running = False

    async def start(self) -> None:
        """Start health checks"""
        self._running = True
        self._task = asyncio.create_task(self._check_loop())

    async def stop(self) -> None:
        """Stop health checks"""
        self._running = False
        if self._task:
            await self._task

    def add_check(self, name: str, check: callable) -> None:
        """Add health check"""
        self._checks[name] = check

    async def get_status(self) -> Dict[str, Any]:
        """Get overall health status"""
        status = HealthStatus.HEALTHY
        details = {}

        for name, result in self._results.items():
            details[name] = result
            if result["status"] == HealthStatus.UNHEALTHY:
                status = HealthStatus.UNHEALTHY
            elif result["status"] == HealthStatus.DEGRADED and status != HealthStatus.UNHEALTHY:
                status = HealthStatus.DEGRADED

        return {"status": status, "timestamp": datetime.utcnow(), "details": details}

    async def _check_loop(self) -> None:
        """Health check loop"""
        while self._running:
            try:
                for name, check in self._checks.items():
                    try:
                        result = await check()
                        self._results[name] = {
                            "status": result.get("status", HealthStatus.UNHEALTHY),
                            "message": result.get("message", "Check failed"),
                            "timestamp": datetime.utcnow(),
                        }
                    except Exception as e:
                        self._results[name] = {
                            "status": HealthStatus.UNHEALTHY,
                            "message": str(e),
                            "timestamp": datetime.utcnow(),
                        }
            except Exception as e:
                print(f"Health check loop failed: {str(e)}")

            await asyncio.sleep(self._interval)
