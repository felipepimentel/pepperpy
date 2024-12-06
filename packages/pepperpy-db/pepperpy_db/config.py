"""Database configuration."""

from dataclasses import dataclass, field
from typing import Any

from pepperpy_core.base import BaseConfigData


@dataclass
class DatabaseConfig(BaseConfigData):
    """Database configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str = ""

    # Required database fields
    database: str = ""
    user: str = ""
    password: str = ""

    # Optional fields
    enabled: bool = True
    host: str = "localhost"
    port: int = 5432
    ssl: bool = False
    pool_size: int = 10
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if not self.database:
            raise ValueError("database is required")
        if not self.user:
            raise ValueError("user is required")
        if not self.password:
            raise ValueError("password is required")
        if self.port < 1:
            raise ValueError("port must be greater than 0")
        if self.pool_size < 1:
            raise ValueError("pool_size must be greater than 0")
