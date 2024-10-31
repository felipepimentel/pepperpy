"""Configuration management system."""
from typing import Any, Dict, Optional, Union
from pathlib import Path
import os
from dataclasses import dataclass, field
import yaml
import json
from dotenv import load_dotenv

@dataclass
class ConfigSource:
    """Configuration source with priority."""
    name: str
    data: Dict[str, Any]
    priority: int = 0

class ConfigManager:
    """Central configuration manager."""
    
    def __init__(self):
        self._sources: Dict[str, ConfigSource] = {}
        self._cache: Dict[str, Any] = {}
        
    def add_source(
        self,
        name: str,
        data: Dict[str, Any],
        priority: int = 0
    ) -> None:
        """Add a configuration source."""
        self._sources[name] = ConfigSource(name, data, priority)
        self._rebuild_cache()
    
    def load_env(self, prefix: str = "") -> None:
        """Load environment variables."""
        load_dotenv()
        env_vars = {
            k: v for k, v in os.environ.items()
            if not prefix or k.startswith(prefix)
        }
        self.add_source("env", env_vars, priority=100)
    
    def load_yaml(self, path: Union[str, Path], priority: int = 0) -> None:
        """Load YAML configuration file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        self.add_source(str(path), data, priority)
    
    def load_json(self, path: Union[str, Path], priority: int = 0) -> None:
        """Load JSON configuration file."""
        with open(path) as f:
            data = json.load(f)
        self.add_source(str(path), data, priority)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._cache.get(key, default)
    
    def set(self, key: str, value: Any, source: str = "memory") -> None:
        """Set configuration value."""
        if source not in self._sources:
            self._sources[source] = ConfigSource(source, {}, 0)
        self._sources[source].data[key] = value
        self._rebuild_cache()
    
    def _rebuild_cache(self) -> None:
        """Rebuild the configuration cache."""
        # Sort sources by priority
        sorted_sources = sorted(
            self._sources.values(),
            key=lambda s: s.priority,
            reverse=True
        )
        
        # Build cache from highest to lowest priority
        self._cache = {}
        for source in sorted_sources:
            self._cache.update(source.data)

# Global config instance
config = ConfigManager() 