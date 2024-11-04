from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Event:
    """Base event class"""

    name: str
    source: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Optional[Dict[str, Any]] = None


EventHandler = Callable[[Any], None]


class EventBus:
    """Event management system"""

    def __init__(self) -> None:
        self._handlers: Dict[str, List[EventHandler]] = {}

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Subscribe to an event"""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

    def publish(self, event: Event) -> None:
        """Publish an event"""
        handlers = self._handlers.get(event.name, [])
        for handler in handlers:
            handler(event)


class SystemEvents:
    """System event constants"""

    MODULE_INITIALIZING = "system.module.initializing"
    MODULE_INITIALIZED = "system.module.initialized"
    MODULE_SHUTDOWN = "system.module.shutdown"
    APPLICATION_STARTING = "system.app.starting"
    APPLICATION_STARTED = "system.app.started"
    APPLICATION_STOPPING = "system.app.stopping"
    APPLICATION_STOPPED = "system.app.stopped"


@dataclass
class ModuleEvent(Event):
    """Module lifecycle event"""

    module_name: str
    status: str
