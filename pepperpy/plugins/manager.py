"""Plugin system for extending functionality."""
from typing import Dict, Any, Optional, Type
import importlib
import pkg_resources
from pathlib import Path

class PluginManager:
    """Manage Pepperpy plugins."""
    
    def __init__(self):
        self.plugins: Dict[str, Any] = {}
        self.hooks: Dict[str, list] = {}
        
    def register_plugin(self, name: str, plugin: Any) -> None:
        """Register a plugin."""
        self.plugins[name] = plugin
        
    def discover_plugins(self) -> None:
        """Discover installed plugins."""
        for entry_point in pkg_resources.iter_entry_points("pepperpy.plugins"):
            try:
                plugin = entry_point.load()
                self.register_plugin(entry_point.name, plugin)
            except Exception as e:
                print(f"Error loading plugin {entry_point.name}: {e}")
                
    def register_hook(self, event: str, callback: callable) -> None:
        """Register a hook for an event."""
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)
        
    async def trigger_hook(self, event: str, **kwargs) -> list:
        """Trigger all hooks for an event."""
        results = []
        if event in self.hooks:
            for callback in self.hooks[event]:
                try:
                    result = await callback(**kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Error in hook {callback.__name__}: {e}")
        return results 