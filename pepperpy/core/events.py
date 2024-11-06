import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union

# Tipos de handlers
SyncHandler = Callable[["Event"], None]
AsyncHandler = Callable[["Event"], Awaitable[None]]
EventHandler = Union[SyncHandler, AsyncHandler]


@dataclass
class Event:
    """Evento base"""

    name: str
    source: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.data is None:
            self.data = {}


class EventBus:
    """
    Sistema de eventos com suporte a handlers síncronos e assíncronos
    """

    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Obtém loop de eventos"""
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Registra handler para um evento"""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: EventHandler) -> None:
        """Remove handler de um evento"""
        if event_name in self._handlers:
            self._handlers[event_name] = [
                h for h in self._handlers[event_name] if h != handler
            ]

    async def publish(self, event: Event) -> None:
        """Publica um evento"""
        handlers = self._handlers.get(event.name, [])

        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    await self.loop.run_in_executor(None, handler, event)
            except Exception as e:
                # Log error but don't stop event propagation
                print(f"Error in event handler: {str(e)}")

    async def publish_many(self, events: List[Event]) -> None:
        """Publica múltiplos eventos"""
        await asyncio.gather(*[self.publish(event) for event in events])

    def clear_handlers(self, event_name: Optional[str] = None) -> None:
        """Limpa handlers de eventos"""
        if event_name:
            self._handlers.pop(event_name, None)
        else:
            self._handlers.clear()


class SystemEvents:
    """Eventos do sistema"""

    # Lifecycle events
    STARTUP = "system.startup"
    SHUTDOWN = "system.shutdown"

    # Module events
    MODULE_INIT = "system.module.init"
    MODULE_READY = "system.module.ready"
    MODULE_ERROR = "system.module.error"

    # State events
    STATE_CHANGED = "system.state.changed"
    CONFIG_CHANGED = "system.config.changed"

    # Error events
    ERROR = "system.error"
    WARNING = "system.warning"


class StateChangeEvent:
    """Evento de mudança de estado"""

    def __init__(self, key: str, old_value: Any, new_value: Any, source: str):
        self.event = Event(
            name=SystemEvents.STATE_CHANGED,
            source=source,
            data={
                "key": key,
                "old_value": old_value,
                "new_value": new_value
            }
        )

    @property
    def key(self) -> str:
        return self.event.data["key"]

    @property
    def old_value(self) -> Any:
        return self.event.data["old_value"]

    @property
    def new_value(self) -> Any:
        return self.event.data["new_value"]


class ErrorEvent:
    """Evento de erro"""

    def __init__(self, error: Exception, source: str):
        self.event = Event(
            name=SystemEvents.ERROR,
            source=source,
            data={
                "error_type": type(error).__name__,
                "error_message": str(error)
            }
        )
        self.error = error

    @property
    def error_type(self) -> str:
        return self.event.data["error_type"]

    @property
    def error_message(self) -> str:
        return self.event.data["error_message"]
