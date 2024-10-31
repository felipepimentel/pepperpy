"""Plugin system implementation."""
from typing import Dict, Any, Optional, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass
from ..core.config import Config

@dataclass
class PluginMetadata:
    """Plugin metadata."""
    name: str
    version: str
    description: str
    author: str
    dependencies: Dict[str, str] = None

class PluginInterface(ABC):
    """Base interface for plugins."""
    
    @abstractmethod
    def initialize(self, config: Config) -> None:
        """Initialize plugin with configuration."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Cleanup plugin resources."""
        pass
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        pass

class PluginManager:
    """Plugin management system."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._plugins: Dict[str, PluginInterface] = {}
        self._hooks: Dict[str, list] = {}
    
    def register(self, plugin: Type[PluginInterface]) -> None:
        """Register a new plugin."""
        instance = plugin()
        metadata = instance.metadata
        
        if metadata.name in self._plugins:
            raise ValueError(f"Plugin {metadata.name} already registered")
        
        instance.initialize(self.config)
        self._plugins[metadata.name] = instance
    
    def unregister(self, name: str) -> None:
        """Unregister a plugin."""
        if plugin := self._plugins.get(name):
            plugin.shutdown()
            del self._plugins[name]
    
    def get_plugin(self, name: str) -> Optional[PluginInterface]:
        """Get plugin by name."""
        return self._plugins.get(name)
    
    def register_hook(self, event: str, callback: callable) -> None:
        """Register event hook."""
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(callback)
    
    async def trigger_event(self, event: str, *args, **kwargs) -> None:
        """Trigger event hooks."""
        for callback in self._hooks.get(event, []):
            await callback(*args, **kwargs) 