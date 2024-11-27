"""Configuration settings implementation"""

from pathlib import Path
from typing import Optional

from pydantic import ConfigDict

from ..base.types import JsonDict
from .base import BaseConfig


class Settings(BaseConfig):
    """Global settings configuration"""

    env: str = "development"
    debug: bool = False
    config_dir: Path = Path("config")
    log_level: str = "INFO"
    metadata: JsonDict = {}
    model_config = ConfigDict(frozen=True)


def load_settings(config_path: Optional[Path] = None) -> Settings:
    """Load settings from configuration file"""
    # Default settings
    settings_data = {
        "name": "pepperpy",
        "env": "development",
        "debug": False,
        "config_dir": "config",
        "log_level": "INFO",
        "metadata": {},
    }

    # Load from file if provided
    if config_path and config_path.exists():
        # TODO: Implement file loading
        pass

    return Settings(**settings_data)
