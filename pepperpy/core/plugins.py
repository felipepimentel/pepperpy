from typing import Optional, Type, Dict, Any, Protocol
from dataclasses import dataclass
from .application import Application

@dataclass
class PluginMetadata:
    """Plugin metadata."""
    name: str
    version: str
    description: str
    author: Optional[str] = None
    dependencies: Optional[List[str]] = None

class Plugin(Protocol):
    """Base plugin protocol."""
    
    @property
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        ...
    
    async def initialize(self, app: Application) -> None:
        """Initialize plugin."""
        ...
    
    async def cleanup(self) -> None:
        """Cleanup plugin resources."""
        ...

class PluginManager:
    """Plugin management system."""
    
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._app: Optional[Application] = None
        
    async def register(self, plugin_class: Type[Plugin]) -> None:
        """Register a plugin."""
        plugin = plugin_class()
        metadata = plugin.metadata
        
        if metadata.name in self._plugins:
            raise ValueError(f"Plugin '{metadata.name}' already registered")
            
        # Check dependencies
        if deps := metadata.dependencies:
            missing = [d for d in deps if d not in self._plugins]
            if missing:
                raise ValueError(
                    f"Plugin '{metadata.name}' requires missing plugins: {missing}"
                )
        
        self._plugins[metadata.name] = plugin
        
        # Initialize if app is available
        if self._app:
            await self._initialize_plugin(plugin)
    
    async def initialize_all(self, app: Application) -> None:
        """Initialize all plugins."""
        self._app = app
        
        for plugin in self._plugins.values():
            await self._initialize_plugin(plugin)
    
    async def _initialize_plugin(self, plugin: Plugin) -> None:
        """Initialize a specific plugin."""
        try:
            await plugin.initialize(self._app)
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize plugin '{plugin.metadata.name}': {e}"
            )
    
    def get(self, name: str) -> Plugin:
        """Get plugin by name."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not found")
        return self._plugins[name]
    
    async def cleanup(self) -> None:
        """Cleanup all plugins."""
        for plugin in self._plugins.values():
            await plugin.cleanup() 