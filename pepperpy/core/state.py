"""State management implementation"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Generic, List, Optional, Set, TypeVar

from .exceptions import CoreError
from .module import BaseModule, ModuleMetadata

T = TypeVar("T")


class StateError(CoreError):
    """State management error"""

    pass


class StateEvent(Enum):
    """State change events"""

    UPDATED = "updated"
    RESET = "reset"
    CLEARED = "cleared"


@dataclass
class StateChange(Generic[T]):
    """State change information"""

    key: str
    old_value: Optional[T]
    new_value: Optional[T]
    timestamp: datetime = field(default_factory=datetime.utcnow)


class StateStore(BaseModule):
    """Global state management"""

    def __init__(self):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="state",
            version="1.0.0",
            description="Global state management",
            dependencies=[],
            config={},
        )
        self._state: Dict[str, Any] = {}
        self._listeners: Dict[str, Set[Callable]] = {}
        self._history: List[StateChange] = []
        self._max_history = 1000
        self._lock = asyncio.Lock()

    async def _setup(self) -> None:
        """Initialize state store"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup state store"""
        self._state.clear()
        self._listeners.clear()
        self._history.clear()

    async def get(self, key: str, default: Any = None) -> Any:
        """Get state value"""
        async with self._lock:
            return self._state.get(key, default)

    async def set(self, key: str, value: Any) -> None:
        """Set state value"""
        async with self._lock:
            old_value = self._state.get(key)
            self._state[key] = value

            # Record change
            change = StateChange(key, old_value, value)
            self._record_change(change)

            # Notify listeners
            await self._notify_listeners(key, StateEvent.UPDATED, change)

    async def update(self, updates: Dict[str, Any]) -> None:
        """Batch update state"""
        async with self._lock:
            changes = []
            for key, value in updates.items():
                old_value = self._state.get(key)
                self._state[key] = value
                changes.append(StateChange(key, old_value, value))

            # Record changes
            for change in changes:
                self._record_change(change)

            # Notify listeners
            for change in changes:
                await self._notify_listeners(change.key, StateEvent.UPDATED, change)

    async def delete(self, key: str) -> None:
        """Delete state value"""
        async with self._lock:
            if key in self._state:
                old_value = self._state.pop(key)
                change = StateChange(key, old_value, None)
                self._record_change(change)
                await self._notify_listeners(key, StateEvent.CLEARED, change)

    async def clear(self) -> None:
        """Clear all state"""
        async with self._lock:
            self._state.clear()
            self._history.clear()
            for key in list(self._listeners.keys()):
                await self._notify_listeners(key, StateEvent.CLEARED, None)

    async def reset(self, initial_state: Dict[str, Any]) -> None:
        """Reset state to initial values"""
        async with self._lock:
            old_state = self._state.copy()
            self._state = initial_state.copy()

            # Record changes
            for key in set(old_state) | set(initial_state):
                change = StateChange(key, old_state.get(key), initial_state.get(key))
                self._record_change(change)

            # Notify listeners
            for key in self._listeners:
                await self._notify_listeners(key, StateEvent.RESET, None)

    def subscribe(self, key: str, listener: Callable) -> None:
        """Subscribe to state changes"""
        if key not in self._listeners:
            self._listeners[key] = set()
        self._listeners[key].add(listener)

    def unsubscribe(self, key: str, listener: Callable) -> None:
        """Unsubscribe from state changes"""
        if key in self._listeners:
            self._listeners[key].discard(listener)
            if not self._listeners[key]:
                del self._listeners[key]

    def get_history(
        self, key: Optional[str] = None, limit: Optional[int] = None
    ) -> List[StateChange]:
        """Get state change history"""
        history = self._history
        if key:
            history = [change for change in history if change.key == key]
        if limit:
            history = history[-limit:]
        return history

    def _record_change(self, change: StateChange) -> None:
        """Record state change"""
        self._history.append(change)
        if len(self._history) > self._max_history:
            self._history.pop(0)

    async def _notify_listeners(
        self, key: str, event: StateEvent, change: Optional[StateChange]
    ) -> None:
        """Notify state change listeners"""
        if key in self._listeners:
            for listener in self._listeners[key]:
                try:
                    await listener(event, change)
                except Exception as e:
                    print(f"Error in state listener: {str(e)}")


# Global state store instance
state = StateStore()
