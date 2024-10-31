"""Event dispatching system."""
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio
import json

@dataclass
class Event:
    """Event data container."""
    name: str
    data: Any
    timestamp: datetime = None
    
    def __post_init__(self):
        self.timestamp = self.timestamp or datetime.now()
    
    def to_json(self) -> str:
        """Convert event to JSON string."""
        return json.dumps({
            "name": self.name,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        })

class EventDispatcher:
    """Event dispatcher implementation."""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._middleware: List[Callable] = []
        self._history: List[Event] = []
        self._max_history: int = 1000
    
    def subscribe(self, event_name: str, handler: Callable) -> None:
        """Subscribe to an event."""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
    
    def unsubscribe(self, event_name: str, handler: Callable) -> None:
        """Unsubscribe from an event."""
        if handlers := self._handlers.get(event_name):
            self._handlers[event_name] = [h for h in handlers if h != handler]
    
    def add_middleware(self, middleware: Callable) -> None:
        """Add event middleware."""
        self._middleware.append(middleware)
    
    async def dispatch(self, event: Event) -> None:
        """Dispatch event to handlers."""
        # Apply middleware
        for middleware in self._middleware:
            event = await middleware(event)
            if event is None:
                return
        
        # Store in history
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)
        
        # Call handlers
        handlers = self._handlers.get(event.name, [])
        await asyncio.gather(
            *[handler(event) for handler in handlers]
        )
    
    def get_history(
        self,
        event_name: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Event]:
        """Get event history."""
        history = self._history
        if event_name:
            history = [e for e in history if e.name == event_name]
        if limit:
            history = history[-limit:]
        return history 