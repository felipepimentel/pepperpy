"""Resource management utilities"""

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict

from .exceptions import CoreError


class ResourceManager:
    """Manager for async resources"""

    def __init__(self):
        self._resources: Dict[str, Any] = {}
        self._initializers: Dict[str, callable] = {}

    async def initialize(self, name: str) -> Any:
        """Initialize resource

        Args:
            name: Resource identifier

        Returns:
            Any: Initialized resource

        Raises:
            CoreError: If resource initializer not found
        """
        if name not in self._resources:
            if name not in self._initializers:
                raise CoreError(f"No initializer for resource: {name}")
            self._resources[name] = await self._initializers[name]()
        return self._resources[name]

    async def cleanup(self) -> None:
        """Cleanup all resources"""
        for resource in self._resources.values():
            if hasattr(resource, "cleanup"):
                await resource.cleanup()
        self._resources.clear()

    @asynccontextmanager
    async def scope(self) -> AsyncIterator["ResourceManager"]:
        """Resource scope context manager

        Returns:
            AsyncIterator[ResourceManager]: Resource manager instance

        Example:
            async with resources.scope() as rm:
                resource = await rm.initialize("my_resource")
        """
        try:
            yield self
        finally:
            await self.cleanup()

    def register_initializer(self, name: str, initializer: callable) -> None:
        """Register resource initializer

        Args:
            name: Resource identifier
            initializer: Async function to initialize resource
        """
        self._initializers[name] = initializer


# Global resource manager instance
resources = ResourceManager()
