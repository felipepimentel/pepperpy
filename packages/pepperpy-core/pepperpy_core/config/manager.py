"""Configuration manager implementation"""

from copy import deepcopy
from pathlib import Path
from typing import Any, Optional, Type, TypeVar, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic import ValidationError as PydanticValidationError

from ..base.module import BaseModule
from ..base.types import JsonDict
from ..exceptions import ValidationError
from .base import BaseConfig

T = TypeVar("T", bound=BaseConfig)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries"""
    result = deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


class ConfigManagerConfig(BaseModel):
    """Configuration manager configuration"""

    model_config = ConfigDict(extra="allow")
    env_prefix: str = "PEPPERPY_"
    config_dir: Union[str, Path] = Field(default="config")
    metadata: JsonDict = Field(default_factory=dict)


class ConfigManager(BaseModule[ConfigManagerConfig]):
    """Configuration manager"""

    def __init__(self, config: Optional[ConfigManagerConfig] = None) -> None:
        super().__init__(config or ConfigManagerConfig())
        self._configs: dict[str, Any] = {}

    async def _initialize(self) -> None:
        """Initialize configuration manager"""
        config_dir = Path(self.config.config_dir)
        config_dir.mkdir(parents=True, exist_ok=True)
        self._configs.clear()

    async def _cleanup(self) -> None:
        """Cleanup configuration manager"""
        self._configs.clear()

    def load_config(
        self,
        config_class: Type[T],
        data: dict[str, Any],
        *,
        override: Optional[dict[str, Any]] = None,
    ) -> T:
        """Load configuration"""
        self._ensure_initialized()

        if override:
            merged_data = deep_merge(data, override)
        else:
            merged_data = data

        try:
            config = config_class(**merged_data)
        except PydanticValidationError as e:
            raise ValidationError(str(e), cause=e)

        self._configs[config_class.__name__] = config
        return config

    def set_config(self, config: Union[BaseConfig, dict[str, Any]]) -> None:
        """Set configuration"""
        self._ensure_initialized()
        if isinstance(config, dict):
            self._configs.update(config)
        else:
            self._configs[config.__class__.__name__] = config

    def get_config(self, key: str) -> Any:
        """Get configuration value"""
        self._ensure_initialized()
        return self._configs.get(key)


__all__ = [
    "ConfigManager",
    "ConfigManagerConfig",
]
