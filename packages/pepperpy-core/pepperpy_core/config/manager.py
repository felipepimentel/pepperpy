"""Configuration manager."""

from typing import Any, TypeVar

from pydantic import BaseModel

from .types import ConfigManagerConfig

T = TypeVar("T", bound=BaseModel)


class ConfigManager:
    """Configuration manager implementation."""

    def __init__(self, config: ConfigManagerConfig) -> None:
        """Initialize configuration manager.

        Args:
            config: Configuration manager configuration
        """
        self.config = config
        self._initialized = False
        self._configs: dict[str, Any] = {}

    async def initialize(self) -> None:
        """Initialize configuration manager."""
        if self._initialized:
            return
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup configuration manager."""
        if not self._initialized:
            return
        self._configs.clear()
        self._initialized = False

    async def get_config(self, key: str, config_type: type[T]) -> T | None:
        """Get configuration by key.

        Args:
            key: Configuration key
            config_type: Configuration type

        Returns:
            Configuration instance if found, None otherwise
        """
        if not self._initialized:
            return None

        # Aqui você implementaria a lógica real de busca da configuração
        # Por enquanto retornamos um valor padrão para teste
        return config_type()
