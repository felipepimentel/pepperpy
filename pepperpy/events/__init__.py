"""Event system for inter-module communication."""
from typing import Any, Callable, Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import logging
from enum import Enum

class EventPriority(Enum):
    """Priority levels for event handlers."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class Event:
    """Base event class."""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    source: Optional[str] = None
    priority: EventPriority = EventPriority.NORMAL

@dataclass
class EventHandler:
    """Event handler with metadata."""
    callback: Callable
    priority: EventPriority
    filters: Dict[str, Any] = field(default_factory=dict)

class EventBus:
    """Central event bus for application-wide events."""
    
    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._tasks: Set[asyncio.Task] = set()
        self.logger = logging.getLogger(__name__)
    
    def subscribe(
        self,
        event_type: str,
        handler: Callable,
        priority: EventPriority = EventPriority.NORMAL,
        **filters
    ) -> None:
        """Subscribe to an event type with optional filters."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
            
        self._handlers[event_type].append(
            EventHandler(handler, priority, filters)
        )
        
        # Sort handlers by priority
        self._handlers[event_type].sort(
            key=lambda h: h.priority.value,
            reverse=True
        )
    
    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._handlers:
            self._handlers[event_type] = [
                h for h in self._handlers[event_type]
                if h.callback != handler
            ]
    
    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribers."""
        await self._queue.put(event)
    
    async def start(self) -> None:
        """Start processing events."""
        self._running = True
        self._tasks.add(
            asyncio.create_task(self._process_events())
        )
    
    async def stop(self) -> None:
        """Stop processing events."""
        self._running = False
        await self._queue.join()
        
        for task in self._tasks:
            task.cancel()
        
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
    
    def _matches_filters(self, event: Event, filters: Dict[str, Any]) -> bool:
        """Check if event matches handler filters."""
        return all(
            event.data.get(key) == value
            for key, value in filters.items()
        )
    
    async def _process_events(self) -> None:
        """Process events from queue."""
        while self._running:
            try:
                event = await self._queue.get()
                
                if event.type in self._handlers:
                    for handler in self._handlers[event.type]:
                        if self._matches_filters(event, handler.filters):
                            try:
                                if asyncio.iscoroutinefunction(handler.callback):
                                    await handler.callback(event)
                                else:
                                    handler.callback(event)
                            except Exception as e:
                                self.logger.error(
                                    f"Error in event handler: {str(e)}",
                                    exc_info=True
                                )
                
                self._queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(
                    f"Error processing event: {str(e)}",
                    exc_info=True
                )

# Global event bus instance
event_bus = EventBus()

# Convenience functions
async def publish(
    event_type: str,
    data: Dict[str, Any],
    priority: EventPriority = EventPriority.NORMAL,
    source: Optional[str] = None
) -> None:
    """Publish an event."""
    event = Event(
        type=event_type,
        data=data,
        priority=priority,
        source=source
    )
    await event_bus.publish(event)

def subscribe(
    event_type: str,
    priority: EventPriority = EventPriority.NORMAL,
    **filters
) -> Callable:
    """Decorator to subscribe a function to an event."""
    def decorator(func: Callable) -> Callable:
        event_bus.subscribe(event_type, func, priority, **filters)
        return func
    return decorator