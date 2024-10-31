"""Plugin system for AI capabilities."""
from typing import Dict, Any, Type, Optional
from abc import ABC, abstractmethod
import importlib
import pkg_resources
from loguru import logger

class AIPlugin(ABC):
    """Base class for AI plugins."""
    
    @abstractmethod
    def initialize(self, **kwargs) -> None:
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        pass

class PluginManager:
    """Manages AI plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, AIPlugin] = {}
        self._discover_plugins()
    
    def _discover_plugins(self):
        """Discover installed plugins."""
        for entry_point in pkg_resources.iter_entry_points('pepperpy.ai.plugins'):
            try:
                plugin_class = entry_point.load()
                self._plugins[entry_point.name] = plugin_class()
            except Exception as e:
                logger.warning(f"Failed to load plugin {entry_point.name}: {e}")
    
    def get_plugin(self, name: str) -> Optional[AIPlugin]:
        """Get a plugin by name."""
        return self._plugins.get(name)
    
    def initialize_all(self, **kwargs):
        """Initialize all plugins."""
        for plugin in self._plugins.values():
            plugin.initialize(**kwargs)
    
    def cleanup_all(self):
        """Cleanup all plugins."""
        for plugin in self._plugins.values():
            plugin.cleanup() 