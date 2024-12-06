"""Configuration manager."""

import json
import os
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from .types import ConfigManagerConfig

T = TypeVar("T", bound=BaseModel)


class ConfigManager:
    """Configuration manager."""

    def __init__(self, config: ConfigManagerConfig) -> None:
        """Initialize configuration manager."""
        self.config = config
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize manager."""
        if not self._initialized:
            await self._setup()
            self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup manager resources."""
        if self._initialized:
            await self._teardown()
            self._initialized = False

    async def _setup(self) -> None:
        """Setup manager resources."""
        os.makedirs(self.config.config_path, exist_ok=True)

    async def _teardown(self) -> None:
        """Teardown manager resources."""
        pass

    async def get_config(self, name: str, config_type: type[T]) -> T | None:
        """Get configuration by name.

        Args:
            name: Configuration name
            config_type: Configuration type

        Returns:
            Configuration instance or None if not found

        Raises:
            ValueError: If config file not found
        """
        config_path = Path(self.config.config_path) / f"{name}.json"
        if not config_path.exists():
            raise ValueError(f"Config file not found: {name}")

        config_data = json.loads(config_path.read_text())
        return config_type.model_validate(config_data)
