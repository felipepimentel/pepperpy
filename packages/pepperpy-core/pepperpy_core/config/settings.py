"""Settings module for PepperPy Core."""

import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv

    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


class Environment(Enum):
    """Environment enum."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

    @classmethod
    def from_string(cls, value: str) -> "Environment":
        """Create Environment from string.

        Args:
            value: Environment string value

        Returns:
            Environment enum value

        Raises:
            ValueError: If value is invalid
        """
        try:
            return cls(value.lower())
        except ValueError:
            return cls.DEVELOPMENT


@dataclass
class Settings:
    """Settings class."""

    debug: bool | None = None
    testing: bool | None = None
    env_name: str | None = None
    environment: Environment | None = None

    # Paths
    base_path: Path = field(default_factory=lambda: Path.cwd())
    config_path: Path = field(default_factory=lambda: Path.cwd() / "config")

    def __post_init__(self) -> None:
        """Post init hook."""
        if HAS_DOTENV:
            load_dotenv()

        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.testing = os.getenv("TESTING", "false").lower() == "true"
        self.env_name = os.getenv("ENV_NAME", "development")
        self.environment = Environment.from_string(self.env_name)

    def get_path(self, *parts: str) -> Path:
        """Get path relative to base path.

        Args:
            *parts: Path parts

        Returns:
            Absolute path
        """
        return self.base_path.joinpath(*parts)

    def get_config(self, name: str) -> dict[str, Any]:
        """Get configuration by name.

        Args:
            name: Configuration name

        Returns:
            Configuration dictionary
        """
        config_file = self.config_path / f"{name}.json"
        if not config_file.exists():
            return {}

        return {}  # TODO: Implement config loading


settings = Settings()
