"""Logging configuration."""

from dataclasses import dataclass, field
from typing import Any

from pepperpy_core.logging.types import LogLevel


@dataclass
class LogConfig:
    """Log configuration."""

    name: str
    level: str = str(LogLevel.INFO.value)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Post initialization."""
        if self.metadata is None:
            self.metadata = {}
