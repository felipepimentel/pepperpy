"""Metrics collection and reporting"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Metric:
    """Metric data point"""

    name: str
    value: float
    tags: Dict[str, str]
    timestamp: datetime
    type: str = "gauge"  # gauge, counter, histogram


class MetricsReporter:
    """Metrics collection and reporting"""

    def __init__(self, interval: int = 10):
        self._metrics: List[Metric] = []
        self._interval = interval
        self._task = None
        self._running = False
        self._handlers = []

    async def start(self) -> None:
        """Start metrics reporting"""
        self._running = True
        self._task = asyncio.create_task(self._report_loop())

    async def stop(self) -> None:
        """Stop metrics reporting"""
        self._running = False
        if self._task:
            await self._task

    def add_handler(self, handler: callable) -> None:
        """Add metrics handler"""
        self._handlers.append(handler)

    async def record(
        self, name: str, value: float, tags: Optional[Dict[str, str]] = None, type: str = "gauge"
    ) -> None:
        """Record metric"""
        metric = Metric(
            name=name, value=value, tags=tags or {}, timestamp=datetime.utcnow(), type=type
        )
        self._metrics.append(metric)

    async def _report_loop(self) -> None:
        """Metrics reporting loop"""
        while self._running:
            try:
                if self._metrics:
                    metrics = self._metrics.copy()
                    self._metrics.clear()

                    for handler in self._handlers:
                        try:
                            await handler(metrics)
                        except Exception as e:
                            print(f"Metrics handler failed: {str(e)}")

            except Exception as e:
                print(f"Metrics reporting failed: {str(e)}")

            await asyncio.sleep(self._interval)
