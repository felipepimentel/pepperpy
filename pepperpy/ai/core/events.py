"""Event system for AI operations."""
from typing import Dict, Any, Callable, List
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
from loguru import logger

@dataclass
class AIEvent:
    """Represents an AI-related event."""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "ai"

class EventManager:
    """Manages AI events."""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._queue = asyncio.Queue()
        self._running = False
    
    async def start(self):
        """Start event processing."""
        self._running = True
        while self._running:
            event = await self._queue.get()
            await self._process_event(event)
            self._queue.task_done()
    
    async def stop(self):
        """Stop event processing."""
        self._running = False
        await self._queue.join()
    
    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
    
    async def emit(self, event: AIEvent):
        """Emit an event."""
        await self._queue.put(event)
    
    async def _process_event(self, event: AIEvent):
        """Process a single event."""
        handlers = self._handlers.get(event.type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error in event handler: {e}")

# Global event manager
event_manager = EventManager() 