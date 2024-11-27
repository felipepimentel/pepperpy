"""Registry manager implementation"""

from typing import Any, Dict, Optional, Type

from pydantic import BaseModel

from ..module import BaseModule
from .types import Registration, RegistryEntry


class RegistryConfig(BaseModel):
    """Registry configuration"""

    auto_discover: bool = True
    plugins_enabled: bool = True


class RegistryManager(BaseModule[RegistryConfig]):
    """Registry manager implementation"""

    def __init__(self, config: RegistryConfig) -> None:
        super().__init__(config)
        self._registry: Dict[str, RegistryEntry] = {}

    async def _initialize(self) -> None:
        """Initialize registry"""
        if self.config.auto_discover:
            await self._discover_components()

    async def _cleanup(self) -> None:
        """Cleanup registry"""
        self._registry.clear()

    async def _discover_components(self) -> None:
        """Discover available components"""
        # Implementar descoberta de componentes
        pass

    def register(self, registration: Registration) -> None:
        """Register component"""
        self._ensure_initialized()
        entry = RegistryEntry(
            name=registration.name,
            component_type=registration.component_type,
            factory=registration.factory,
            metadata=registration.metadata,
        )
        self._registry[registration.name] = entry

    def get_component(self, name: str) -> Optional[Type[Any]]:
        """Get registered component"""
        self._ensure_initialized()
        entry = self._registry.get(name)
        return entry.component_type if entry else None
