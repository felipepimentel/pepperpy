"""Plugin system."""
from typing import Dict, Any, Type, Optional, List
import importlib
import pkg_resources
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class PluginInfo:
    """Plugin metadata."""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str]

class Plugin(ABC):
    """Base plugin interface."""
    
    @abstractmethod
    def initialize(self, **kwargs) -> None:
        """Initialize plugin."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        pass
    
    @property
    @abstractmethod
    def info(self) -> PluginInfo:
        """Get plugin information."""
        pass

class PluginRegistry:
    """Plugin registry and manager."""
    
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._enabled: Dict[str, bool] = {}
    
    def register(self, plugin: Plugin) -> None:
        """Register a plugin."""
        info = plugin.info
        if info.name in self._plugins:
            raise ValueError(f"Plugin {info.name} already registered")
            
        # Check dependencies
        for dep in info.dependencies:
            if dep not in self._plugins:
                raise ValueError(f"Missing dependency: {dep}")
        
        self._plugins[info.name] = plugin
        self._enabled[info.name] = True
    
    def discover(self) -> None:
        """Discover installed plugins."""
        for entry_point in pkg_resources.iter_entry_points('pepperpy.plugins'):
            try:
                plugin_class = entry_point.load()
                plugin = plugin_class()
                self.register(plugin)
            except Exception as e:
                # Log error but continue
                print(f"Failed to load plugin {entry_point.name}: {e}")
    
    def enable(self, name: str) -> None:
        """Enable a plugin."""
        if name not in self._plugins:
            raise ValueError(f"Plugin not found: {name}")
        self._enabled[name] = True
        self._plugins[name].initialize()
    
    def disable(self, name: str) -> None:
        """Disable a plugin."""
        if name not in self._plugins:
            raise ValueError(f"Plugin not found: {name}")
        self._enabled[name] = False
        self._plugins[name].cleanup()
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name."""
        return self._plugins.get(name)
    
    def list_plugins(self) -> List[PluginInfo]:
        """List all registered plugins."""
        return [p.info for p in self._plugins.values()]

# Global plugin registry
plugin_registry = PluginRegistry() 