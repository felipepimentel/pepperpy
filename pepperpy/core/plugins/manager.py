"""Plugin manager implementation"""

from typing import Any

from pepperpy.core.module import BaseModule

from .exceptions import PluginError
from .types import Plugin, PluginConfig


class PluginManager(BaseModule[PluginConfig]):
    """Plugin manager implementation"""

    def __init__(self, config: PluginConfig) -> None:
        super().__init__(config)
        self._plugins: dict[str, Plugin] = {}

    async def _initialize(self) -> None:
        """Initialize plugin manager"""
        if self.config.auto_load:
            await self._load_plugins()

    async def _cleanup(self) -> None:
        """Cleanup plugin resources"""
        for plugin in self._plugins.values():
            await plugin.cleanup()
        self._plugins.clear()

    async def _load_plugins(self) -> None:
        """Load plugins"""
        try:
            # Implement plugin loading logic here
            pass
        except Exception as e:
            raise PluginError(f"Failed to load plugins: {e}", cause=e)

    async def register_plugin(self, name: str, plugin: Plugin) -> None:
        """Register plugin"""
        if not self._initialized:
            await self.initialize()

        if name in self._plugins:
            raise PluginError(f"Plugin {name} already registered")

        try:
            await plugin.initialize()
            self._plugins[name] = plugin
        except Exception as e:
            raise PluginError(f"Failed to register plugin {name}: {e}", cause=e)

    async def execute_plugin(self, name: str, **kwargs: Any) -> Any:
        """Execute plugin"""
        if not self._initialized:
            await self.initialize()

        plugin = self._plugins.get(name)
        if not plugin:
            raise PluginError(f"Plugin {name} not found")

        try:
            return await plugin.execute(**kwargs)
        except Exception as e:
            raise PluginError(f"Failed to execute plugin {name}: {e}", cause=e)

    async def unregister_plugin(self, name: str) -> None:
        """Unregister plugin"""
        if not self._initialized:
            await self.initialize()

        plugin = self._plugins.get(name)
        if not plugin:
            raise PluginError(f"Plugin {name} not found")

        try:
            await plugin.cleanup()
            del self._plugins[name]
        except Exception as e:
            raise PluginError(f"Failed to unregister plugin {name}: {e}", cause=e)
