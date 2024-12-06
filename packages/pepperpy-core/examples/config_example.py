"""Configuration example."""

from dataclasses import dataclass
from typing import Any

from pepperpy_core.base import BaseConfigData
from pepperpy_core.config import BaseConfig


@dataclass
class ExampleConfigData(BaseConfigData):
    """Example configuration data."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    host: str = "localhost"
    port: int = 8080
    debug: bool = False


class ExampleConfig(BaseConfig[ExampleConfigData]):
    """Example configuration implementation."""

    def __init__(self) -> None:
        """Initialize configuration."""
        config = ExampleConfigData(name="example-config")
        super().__init__(config)
        self._data: dict[str, Any] = {}

    async def _setup(self) -> None:
        """Setup configuration resources."""
        # Exemplo simples usando dicionário em memória
        self._data = {
            "host": self.config.host,
            "port": self.config.port,
            "debug": self.config.debug,
        }

    async def _teardown(self) -> None:
        """Cleanup configuration resources."""
        self._data.clear()

    async def load(self, path: str) -> None:
        """Load configuration from file.

        Args:
            path: Path to configuration file
        """
        # Exemplo simples - na prática você carregaria de um arquivo
        self._data = {
            "host": "example.com",
            "port": 443,
            "debug": True,
        }

    async def save(self, path: str) -> None:
        """Save configuration to file.

        Args:
            path: Path to save configuration
        """
        # Exemplo simples - na prática você salvaria em um arquivo
        print(f"Saving configuration to {path}:")
        print(self._data)

    async def get_stats(self) -> dict[str, Any]:
        """Get configuration statistics.

        Returns:
            Configuration statistics
        """
        return {
            "settings_count": len(self._data),
            "has_host": "host" in self._data,
            "has_port": "port" in self._data,
            "debug_enabled": self._data.get("debug", False),
        }


async def main() -> None:
    """Run example."""
    # Create configuration instance
    config = ExampleConfig()

    # Initialize
    await config.initialize()

    try:
        # Load configuration
        await config.load("/etc/example/config.json")

        # Get statistics
        stats = await config.get_stats()
        print("Configuration stats:", stats)

        # Save configuration
        await config.save("/etc/example/config.json")

    finally:
        await config.cleanup()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
