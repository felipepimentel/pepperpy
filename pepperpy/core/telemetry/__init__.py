"""Core telemetry module"""

from abc import ABC, abstractmethod
from typing import Any

from .collectors import TelemetryCollector
from .exceptions import TelemetryError
from .types import Event, Span, TraceContext


class TelemetryProvider(ABC):
    """Base telemetry provider interface"""

    @abstractmethod
    async def record_event(self, event: Event) -> None:
        """Record telemetry event"""
        pass

    @abstractmethod
    async def start_span(self, name: str, **context: Any) -> Span:
        """Start telemetry span"""
        pass

    @abstractmethod
    async def end_span(self, span: Span) -> None:
        """End telemetry span"""
        pass


__all__ = [
    "TelemetryProvider",
    "TelemetryCollector",
    "TelemetryError",
    "Event",
    "Span",
    "TraceContext",
]
