"""Configuration manager implementation"""

from pathlib import Path
from typing import Any

from pepperpy.core.module import BaseModule

from .exceptions import ConfigError
from .types import ConfigManagerConfig, ConfigSource


class ConfigManager(BaseModule[ConfigManagerConfig]):
    """Configuration manager implementation"""

    def __init__(self, config: ConfigManagerConfig) -> None:
        super().__init__(config)
        self._configs: dict[str, dict[str, Any]] = {}

    async def _initialize(self) -> None:
        """Initialize configuration manager"""
        if self.config.auto_load:
            await self._load_configs()

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        self._configs.clear()

    async def _load_configs(self) -> None:
        """Load configurations from sources"""
        try:
            for source in self.config.sources:
                await self._load_source(source)
        except Exception as e:
            raise ConfigError(f"Failed to load configurations: {e}", cause=e)

    async def _load_source(self, source: ConfigSource) -> None:
        """Load configuration from source"""
        try:
            if source.path:
                await self._load_from_file(source.name, source.path)
            elif source.data:
                self._configs[source.name] = source.data
        except Exception as e:
            raise ConfigError(f"Failed to load source {source.name}: {e}", cause=e)

    async def _load_from_file(self, name: str, path: Path) -> None:
        """Load configuration from file"""
        try:
            # Implement file loading logic here
            # Example: YAML, JSON, etc.
            pass
        except Exception as e:
            raise ConfigError(f"Failed to load file {path}: {e}", cause=e)

    async def get_config(self, source: str, key: str) -> Any:
        """Get configuration value"""
        if not self._initialized:
            await self.initialize()

        config = self._configs.get(source)
        if not config:
            raise ConfigError(f"Configuration source {source} not found")

        value = config.get(key)
        if value is None:
            raise ConfigError(f"Configuration key {key} not found in {source}")

        return value

    async def set_config(self, source: str, key: str, value: Any) -> None:
        """Set configuration value"""
        if not self._initialized:
            await self.initialize()

        if source not in self._configs:
            self._configs[source] = {}

        self._configs[source][key] = value
