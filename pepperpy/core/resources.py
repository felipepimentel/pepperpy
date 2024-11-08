"""Resource management and cleanup system"""

import asyncio
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, TypeVar

T = TypeVar("T")


class ResourceState(Enum):
    """Resource lifecycle states"""

    UNINITIALIZED = auto()
    INITIALIZING = auto()
    READY = auto()
    ERROR = auto()
    CLEANING = auto()
    CLEANED = auto()


@dataclass
class Resource:
    """Managed resource with lifecycle"""

    name: str
    initialize: Callable[[], Any]
    cleanup: Callable[[], Any]
    dependencies: List[str] = field(default_factory=list)
    state: ResourceState = ResourceState.UNINITIALIZED
    instance: Any = None
    error: Optional[Exception] = None


class ResourceManager:
    """Manager for resource lifecycle"""

    def __init__(self):
        self._resources: Dict[str, Resource] = {}
        self._logger = logging.getLogger(__name__)
        self._lock = asyncio.Lock()

    def register(
        self,
        name: str,
        initialize: Callable[[], Any],
        cleanup: Callable[[], Any],
        dependencies: List[str] = None,
    ) -> None:
        """Register resource with lifecycle handlers"""
        self._resources[name] = Resource(
            name=name, initialize=initialize, cleanup=cleanup, dependencies=dependencies or []
        )

    async def initialize(self) -> None:
        """Initialize all resources in dependency order"""
        async with self._lock:
            sorted_resources = self._resolve_dependencies()

            for resource in sorted_resources:
                try:
                    resource.state = ResourceState.INITIALIZING
                    if asyncio.iscoroutinefunction(resource.initialize):
                        resource.instance = await resource.initialize()
                    else:
                        resource.instance = resource.initialize()
                    resource.state = ResourceState.READY
                    self._logger.info(f"Initialized resource: {resource.name}")
                except Exception as e:
                    resource.state = ResourceState.ERROR
                    resource.error = e
                    self._logger.error(f"Failed to initialize resource {resource.name}: {e}")
                    raise

    async def cleanup(self) -> None:
        """Cleanup all resources in reverse dependency order"""
        async with self._lock:
            for resource in reversed(self._resolve_dependencies()):
                if resource.state not in (ResourceState.READY, ResourceState.ERROR):
                    continue

                try:
                    resource.state = ResourceState.CLEANING
                    if asyncio.iscoroutinefunction(resource.cleanup):
                        await resource.cleanup()
                    else:
                        resource.cleanup()
                    resource.state = ResourceState.CLEANED
                    self._logger.info(f"Cleaned up resource: {resource.name}")
                except Exception as e:
                    self._logger.error(f"Error cleaning up resource {resource.name}: {e}")

    def get(self, name: str) -> Optional[Any]:
        """Get resource instance by name"""
        resource = self._resources.get(name)
        return resource.instance if resource else None

    @asynccontextmanager
    async def scope(self) -> AsyncIterator["ResourceManager"]:
        """Resource scope context manager

        Returns:
            AsyncIterator[ResourceManager]: The resource manager instance
        """
        try:
            await self.initialize()
            yield self
        finally:
            await self.cleanup()

    def _resolve_dependencies(self) -> List[Resource]:
        """Resolve resource dependencies"""
        resolved = []
        visiting = set()

        def visit(resource: Resource):
            if resource.name in visiting:
                raise ValueError(f"Circular dependency detected: {resource.name}")
            if resource in resolved:
                return

            visiting.add(resource.name)

            for dep in resource.dependencies:
                if dep not in self._resources:
                    raise ValueError(f"Missing dependency {dep} for resource {resource.name}")
                visit(self._resources[dep])

            visiting.remove(resource.name)
            resolved.append(resource)

        for resource in self._resources.values():
            visit(resource)

        return resolved
