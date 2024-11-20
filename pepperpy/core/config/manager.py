"""Configuration manager implementation"""

from typing import Any, Optional, TypeVar

from .settings import Settings, settings

ConfigT = TypeVar("ConfigT")


class ConfigManager:
    """Configuration manager singleton"""

    _instance: Optional["ConfigManager"] = None
    _settings: Settings

    def __new__(cls) -> "ConfigManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = settings
        return cls._instance

    @classmethod
    def get_settings(cls) -> Settings:
        """Get global settings"""
        return cls().settings

    @property
    def settings(self) -> Settings:
        """Get settings instance"""
        return self._settings

    def get_config(self, config_class: type[ConfigT], **overrides: Any) -> ConfigT:
        """Get configuration instance with optional overrides"""
        return config_class(**overrides)


# Global configuration manager instance
config_manager = ConfigManager()
