from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, Type, TypeVar

T = TypeVar("T", bound="BaseConfig")


@dataclass
class BaseConfig:
    """Base configuration class"""

    enabled: bool = True
    debug: bool = False

    @classmethod
    def create(cls: Type[T]) -> "ConfigBuilder[T]":
        """Create a new config builder"""
        return ConfigBuilder(cls)


class ConfigBuilder(Generic[T]):
    """Builder for configurations"""

    def __init__(self, config_class: Type[T]) -> None:
        self._config_class = config_class
        self._values: Dict[str, Any] = {}

    def with_value(self, key: str, value: Any) -> "ConfigBuilder[T]":
        """Set configuration value"""
        self._values[key] = value
        return self

    def build(self) -> T:
        """Build configuration instance"""
        return self._config_class(**self._values)


class ConfigurationProvider(ABC):
    """Base class for configuration providers"""

    @abstractmethod
    def get_config(self, module_name: str) -> Dict[str, Any]:
        """Get configuration for module"""
        pass
