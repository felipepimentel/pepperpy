"""Configuration example"""

from dataclasses import dataclass

from pepperpy_core.config import ConfigManager
from pepperpy_core.module import BaseModule
from pepperpy_core.types import JsonDict


@dataclass
class DatabaseConfig:
    """Database configuration"""

    host: str
    port: int
    name: str
    user: str
    password: str
    pool_size: int = 10
    metadata: JsonDict = {}


@dataclass
class CacheConfig:
    """Cache configuration"""

    url: str
    prefix: str
    ttl: int = 3600
    metadata: JsonDict = {}


@dataclass
class AppConfig:
    """Application configuration"""

    name: str
    debug: bool
    database: DatabaseConfig
    cache: CacheConfig
    settings: JsonDict = {}


class Application(BaseModule[AppConfig]):
    """Example application"""

    async def _initialize(self) -> None:
        """Initialize application"""
        print(f"Initializing {self.config.name}...")
        print("Database config:", self.config.database)
        print("Cache config:", self.config.cache)
        self._metadata["initialized_at"] = "now"

    async def _cleanup(self) -> None:
        """Cleanup application"""
        print(f"Cleaning up {self.config.name}...")


def load_config() -> AppConfig:
    """Load application configuration"""
    # Create config manager
    config_manager = ConfigManager()

    # Base configuration
    base_config = {
        "name": "example",
        "debug": False,
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "example",
            "user": "postgres",
            "password": "secret",
            "pool_size": 10,
            "metadata": {"source": "base"},
        },
        "cache": {
            "url": "redis://localhost",
            "prefix": "example",
            "ttl": 3600,
            "metadata": {"source": "base"},
        },
        "settings": {"feature_flags": {"new_feature": False}},
    }

    # Override configuration
    override_config = {
        "debug": True,
        "database": {"pool_size": 20, "metadata": {"source": "override"}},
        "settings": {"feature_flags": {"new_feature": True}},
    }

    # Load and merge configuration
    return config_manager.load_config(AppConfig, base_config, override=override_config)


async def main() -> None:
    """Run example"""
    # Load configuration
    config = load_config()

    # Create application
    app = Application(config)

    try:
        # Initialize
        await app.initialize()

        # Application is ready
        print("Application is ready!")
        print("Settings:", app.config.settings)
        print("Metadata:", app.metadata)

    finally:
        # Cleanup
        await app.cleanup()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
