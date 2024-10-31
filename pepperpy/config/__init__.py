"""Configuration management system."""
from typing import Any, Dict, Optional, Union, Type
from pathlib import Path
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import yaml
import json
import toml
from configparser import ConfigParser

@dataclass
class ConfigSource:
    """Configuration source with metadata."""
    name: str
    data: Dict[str, Any]
    priority: int = 0
    is_mutable: bool = True
    provider: str = "memory"

class ConfigProvider(ABC):
    """Base class for configuration providers."""
    
    @abstractmethod
    def load(self, source: Union[str, Path]) -> Dict[str, Any]:
        """Load configuration from source."""
        pass
    
    @abstractmethod
    def save(self, data: Dict[str, Any], destination: Union[str, Path]) -> None:
        """Save configuration to destination."""
        pass

class YAMLProvider(ConfigProvider):
    """YAML configuration provider."""
    
    def load(self, source: Union[str, Path]) -> Dict[str, Any]:
        with open(source) as f:
            return yaml.safe_load(f)
    
    def save(self, data: Dict[str, Any], destination: Union[str, Path]) -> None:
        with open(destination, 'w') as f:
            yaml.dump(data, f)

class JSONProvider(ConfigProvider):
    """JSON configuration provider."""
    
    def load(self, source: Union[str, Path]) -> Dict[str, Any]:
        with open(source) as f:
            return json.load(f)
    
    def save(self, data: Dict[str, Any], destination: Union[str, Path]) -> None:
        with open(destination, 'w') as f:
            json.dump(data, f, indent=2)

class TOMLProvider(ConfigProvider):
    """TOML configuration provider."""
    
    def load(self, source: Union[str, Path]) -> Dict[str, Any]:
        with open(source) as f:
            return toml.load(f)
    
    def save(self, data: Dict[str, Any], destination: Union[str, Path]) -> None:
        with open(destination, 'w') as f:
            toml.dump(data, f)

class INIProvider(ConfigProvider):
    """INI configuration provider."""
    
    def load(self, source: Union[str, Path]) -> Dict[str, Any]:
        parser = ConfigParser()
        parser.read(source)
        return {
            section: dict(parser[section])
            for section in parser.sections()
        }
    
    def save(self, data: Dict[str, Any], destination: Union[str, Path]) -> None:
        parser = ConfigParser()
        for section, values in data.items():
            parser[section] = {
                k: str(v) for k, v in values.items()
            }
        with open(destination, 'w') as f:
            parser.write(f)

class Config:
    """Central configuration manager."""
    
    _providers = {
        '.yaml': YAMLProvider(),
        '.yml': YAMLProvider(),
        '.json': JSONProvider(),
        '.toml': TOMLProvider(),
        '.ini': INIProvider()
    }
    
    def __init__(self):
        self._sources: Dict[str, ConfigSource] = {}
        self._cache: Dict[str, Any] = {}
        
    def add_source(
        self,
        name: str,
        data: Dict[str, Any],
        priority: int = 0,
        provider: str = "memory"
    ) -> None:
        """Add a configuration source."""
        self._sources[name] = ConfigSource(
            name=name,
            data=data,
            priority=priority,
            provider=provider
        )
        self._rebuild_cache()
    
    def load_file(
        self,
        path: Union[str, Path],
        priority: int = 0,
        name: Optional[str] = None
    ) -> None:
        """Load configuration from file."""
        path = Path(path)
        if path.suffix not in self._providers:
            raise ValueError(f"Unsupported file type: {path.suffix}")
            
        provider = self._providers[path.suffix]
        data = provider.load(path)
        self.add_source(
            name or str(path),
            data,
            priority,
            provider=path.suffix
        )
    
    def save_to_file(
        self,
        path: Union[str, Path],
        source: Optional[str] = None
    ) -> None:
        """Save configuration to file."""
        path = Path(path)
        if path.suffix not in self._providers:
            raise ValueError(f"Unsupported file type: {path.suffix}")
            
        provider = self._providers[path.suffix]
        data = (
            self._sources[source].data
            if source
            else self._cache
        )
        provider.save(data, path)
    
    def get(
        self,
        key: str,
        default: Any = None,
        source: Optional[str] = None
    ) -> Any:
        """Get configuration value."""
        if source:
            if source not in self._sources:
                raise KeyError(f"Source not found: {source}")
            return self._sources[source].data.get(key, default)
        return self._cache.get(key, default)
    
    def set(
        self,
        key: str,
        value: Any,
        source: str = "memory"
    ) -> None:
        """Set configuration value."""
        if source not in self._sources:
            self._sources[source] = ConfigSource(source, {}, 0)
        elif not self._sources[source].is_mutable:
            raise ValueError(f"Source is immutable: {source}")
            
        self._sources[source].data[key] = value
        self._rebuild_cache()
    
    def _rebuild_cache(self) -> None:
        """Rebuild the configuration cache."""
        sorted_sources = sorted(
            self._sources.values(),
            key=lambda s: s.priority,
            reverse=True
        )
        
        self._cache = {}
        for source in sorted_sources:
            self._cache.update(source.data)

# Global config instance
config = Config() 