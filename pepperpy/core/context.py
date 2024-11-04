from contextlib import contextmanager
from typing import Any, Dict, Optional, Type, TypeVar

from .exceptions import ServiceNotFoundError

T = TypeVar("T")


class Context:
    """Dependency injection container"""

    def __init__(self) -> None:
        self._services: Dict[str, Any] = {}
        self._parent: Optional["Context"] = None

    def register(self, key: str, instance: Any) -> None:
        """Register a service"""
        self._services[key] = instance

    def get(self, key: str, expected_type: Type[T]) -> T:
        """Get a service by key and type"""
        service = self._services.get(key)

        if service is None and self._parent:
            return self._parent.get(key, expected_type)

        if service is None:
            raise ServiceNotFoundError(f"Service not found: {key}")

        if not isinstance(service, expected_type):
            raise TypeError(f"Invalid service type for {key}")

        return service

    @contextmanager
    def scope(self):
        """Create a new context scope"""
        child = Context()
        child._parent = self
        yield child
