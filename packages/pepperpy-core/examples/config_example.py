"""Example demonstrating configuration functionality"""

import asyncio
from pathlib import Path

from pepperpy_core.base.types import JsonDict
from pepperpy_core.config import BaseConfig, ConfigManager, ConfigManagerConfig
from pydantic import ConfigDict, Field


class AppConfig(BaseConfig):
    """Application configuration"""

    name: str
    debug: bool = False
    data_dir: Path = Field(default=Path("data"))
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)


async def main() -> None:
    """Run example"""
    # Create config manager
    manager_config = ConfigManagerConfig(config_dir=Path("config"), env_prefix="APP_")
    manager = ConfigManager(manager_config)

    try:
        # Initialize
        await manager.initialize()

        # Load configuration
        config_data = {
            "name": "example_app",
            "debug": True,
            "data_dir": "data",
            "metadata": {"version": "1.0.0"},
        }

        config = manager.load_config(AppConfig, config_data)
        print(f"Loaded config: {config}")

        # Access configuration
        print(f"App name: {config.name}")
        print(f"Debug mode: {config.debug}")
        print(f"Data directory: {config.data_dir}")
        print(f"Metadata: {config.metadata}")

    finally:
        await manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
