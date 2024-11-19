"""Core configuration module"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from .exceptions import ConfigError, ConfigLoadError, ConfigValidationError
from .manager import ConfigManager, config_manager
from .types import ConfigFormat, ConfigSource, ConfigValue


@dataclass
class ModuleConfig(ABC):
    """Base class for module configurations"""
    name: str
    version: str
    
    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        pass


@dataclass
class AIConfig(ModuleConfig):
    """AI configuration"""
    name: str = "ai"
    version: str = "1.0.0"
    provider: str = "mock"
    api_key: str | None = None
    model: str = "default"
    temperature: float = 0.7
    max_tokens: int = 1000

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "provider": self.provider,
            "api_key": self.api_key,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }


@dataclass
class PepperConfig:
    """Global configuration container"""
    ai: AIConfig | None = None
    modules: dict[str, ModuleConfig] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize modules dict with AI config if provided"""
        if self.ai:
            self.modules["ai"] = self.ai

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "modules": {
                name: config.to_dict() 
                for name, config in self.modules.items()
            }
        }


def load_config() -> PepperConfig:
    """Load global configuration"""
    return PepperConfig()


__all__ = [
    # Classes base
    "ModuleConfig",
    "AIConfig",
    "PepperConfig",
    
    # Gerenciamento
    "ConfigManager",
    "config_manager",
    
    # Exceções
    "ConfigError",
    "ConfigLoadError",
    "ConfigValidationError",
    
    # Tipos
    "ConfigFormat",
    "ConfigSource",
    "ConfigValue",
    
    # Funções
    "load_config",
] 