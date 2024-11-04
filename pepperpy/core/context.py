from typing import Any, Dict, Optional, Type, TypeVar

from .exceptions import ContextError, ServiceNotFoundError

T = TypeVar("T")


class Context:
    """Application context for dependency injection."""

    def __init__(self):
        self._services: Dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """Register a service in the context."""
        if name in self._services:
            raise ContextError(f"Service {name} already registered")
        self._services[name] = service

    def get(self, name: str, expected_type: Optional[Type[T]] = None) -> T:
        """Get a service from the context."""
        service = self._services.get(name)
        if service is None:
            raise ServiceNotFoundError(f"Service {name} not found in context")

        if expected_type and not isinstance(service, expected_type):
            raise ContextError(
                f"Service {name} is of type {type(service)}, expected {expected_type}"
            )

        return service

    def has(self, name: str) -> bool:
        """Check if a service exists in the context."""
        return name in self._services
