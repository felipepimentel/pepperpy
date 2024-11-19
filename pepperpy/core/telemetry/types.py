"""Telemetry type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Event:
    """Telemetry event"""
    name: str
    timestamp: datetime
    duration: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class Span:
    """Telemetry span"""
    id: str
    name: str
    start_time: datetime
    end_time: datetime | None = None
    parent_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceContext:
    """Trace context"""
    trace_id: str
    span_id: str
    parent_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict) 