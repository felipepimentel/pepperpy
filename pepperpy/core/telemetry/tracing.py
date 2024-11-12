"""Distributed tracing implementation"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class Span:
    """Trace span information"""

    id: str
    trace_id: str
    parent_id: Optional[str]
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    tags: Dict[str, str] = None
    error: Optional[Exception] = None


class TracingProvider:
    """Distributed tracing provider"""

    def __init__(self):
        self._spans: Dict[str, Span] = {}
        self._handlers = []
        self._context = {}

    def add_handler(self, handler: callable) -> None:
        """Add tracing handler"""
        self._handlers.append(handler)

    async def start_span(
        self, name: str, parent_id: Optional[str] = None, tags: Optional[Dict[str, str]] = None
    ) -> str:
        """Start new span"""
        span_id = str(uuid.uuid4())
        trace_id = parent_id or span_id

        span = Span(
            id=span_id,
            trace_id=trace_id,
            parent_id=parent_id,
            name=name,
            start_time=datetime.utcnow(),
            tags=tags or {},
        )

        self._spans[span_id] = span
        return span_id

    async def end_span(self, span_id: str, error: Optional[Exception] = None) -> None:
        """End span"""
        if span_id in self._spans:
            span = self._spans[span_id]
            span.end_time = datetime.utcnow()
            span.error = error

            # Notify handlers
            for handler in self._handlers:
                try:
                    await handler(span)
                except Exception as e:
                    print(f"Tracing handler failed: {str(e)}")

            del self._spans[span_id]

    async def add_tag(self, span_id: str, key: str, value: str) -> None:
        """Add tag to span"""
        if span_id in self._spans:
            self._spans[span_id].tags[key] = value

    def get_current_span(self) -> Optional[Span]:
        """Get current span"""
        return self._spans.get(self._context.get("current_span_id"))

    async def clear(self) -> None:
        """Clear all spans"""
        self._spans.clear()
        self._context.clear()
