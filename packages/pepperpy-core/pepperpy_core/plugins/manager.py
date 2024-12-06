"""Plugin manager implementation."""

from dataclasses import dataclass, field
from typing import Any

from ..module import BaseModule
from .config import PluginConfig


@dataclass
class PluginInfo:
    """Plugin information."""

    name: str
    version: str
    enabled: bool = True
    dependencies: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class PluginManager(BaseModule[PluginConfig]):
    """Plugin manager implementation."""

    def __init__(self) -> None:
        """Initialize plugin manager."""
        config = PluginConfig(name="plugin-manager")
        super().__init__(config)
        self._plugins: dict[str, PluginInfo] = {}

    async def _setup(self) -> None:
        """Setup plugin manager."""
        self._plugins.clear()

    async def _teardown(self) -> None:
        """Teardown plugin manager."""
        self._plugins.clear()

    async def register_plugin(self, plugin: PluginInfo) -> None:
        """Register plugin.

        Args:
            plugin: Plugin information
        """
        if not self.is_initialized:
            await self.initialize()
        self._plugins[plugin.name] = plugin

    async def unregister_plugin(self, name: str) -> None:
        """Unregister plugin.

        Args:
            name: Plugin name
        """
        if not self.is_initialized:
            await self.initialize()
        self._plugins.pop(name, None)

    async def get_plugin(self, name: str) -> PluginInfo | None:
        """Get plugin information.

        Args:
            name: Plugin name

        Returns:
            Plugin information if found, None otherwise
        """
        if not self.is_initialized:
            await self.initialize()
        return self._plugins.get(name)

    async def get_stats(self) -> dict[str, Any]:
        """Get plugin manager statistics.

        Returns:
            Plugin manager statistics
        """
        if not self.is_initialized:
            await self.initialize()
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "auto_load": self.config.auto_load,
            "plugins_count": len(self._plugins),
            "enabled_plugins": sum(1 for p in self._plugins.values() if p.enabled),
            "plugin_names": list(self._plugins.keys()),
        }
