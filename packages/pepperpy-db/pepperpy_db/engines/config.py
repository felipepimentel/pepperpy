"""Database engine configuration."""

from dataclasses import dataclass, field
from typing import Any

from pepperpy_core.base import BaseConfigData


@dataclass
class DatabaseEngineConfig(BaseConfigData):
    """Database engine configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: float = 30.0
    pool_recycle: int = 3600
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if self.pool_size < 1:
            raise ValueError("pool_size must be greater than 0")
        if self.max_overflow < 0:
            raise ValueError("max_overflow must be non-negative")
        if self.pool_timeout <= 0:
            raise ValueError("pool_timeout must be greater than 0")
        if self.pool_recycle <= 0:
            raise ValueError("pool_recycle must be greater than 0")
