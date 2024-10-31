"""Async event system with pattern matching."""
from typing import Callable, Dict, List, Optional, Pattern
import re
import asyncio
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Event:
    name: str
    data: dict
    created_at: datetime = None
    
    def __post_init__(self):
        self.created_at = datetime.now()

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._pattern_handlers: List[tuple[Pattern, Callable]] = []
        self._middleware: List[Callable] = []
    
    def on(self, event_pattern: str):
        """Register event handler with pattern matching."""
        def decorator(handler):
            pattern = re.compile(event_pattern)
            self._pattern_handlers.append((pattern, handler))
            return handler
        return decorator
    
    def middleware(self, middleware_func: Callable):
        """Add middleware to event processing."""
        self._middleware.append(middleware_func)
        return middleware_func
    
    async def emit(self, event_name: str, data: dict = None):
        """Emit event to all matching handlers."""
        event = Event(event_name, data or {})
        
        # Process middleware
        for middleware in self._middleware:
            event = await middleware(event)
            if event is None:
                return
        
        # Find matching handlers
        handlers = []
        for pattern, handler in self._pattern_handlers:
            if pattern.match(event_name):
                handlers.append(handler)
        
        # Execute handlers concurrently
        await asyncio.gather(
            *[handler(event) for handler in handlers]
        ) 