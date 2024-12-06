"""Logging example."""

import sys
from dataclasses import dataclass, field
from typing import Any

from pepperpy_core.logging import BaseLogger, LogLevel
from pepperpy_core.types import JsonDict


@dataclass
class LogConfig:
    """Example logger configuration."""

    name: str
    level: LogLevel = LogLevel.INFO
    enabled: bool = True
    metadata: JsonDict = field(default_factory=dict)


class ExampleLogger(BaseLogger):
    """Example logger implementation."""

    def __init__(self, config: LogConfig) -> None:
        """Initialize logger.

        Args:
            config: Logger configuration
        """
        self.config = config

    def log(self, level: LogLevel, message: str, **kwargs: Any) -> None:
        """Log message.

        Args:
            level: Log level
            message: Log message
            **kwargs: Additional log data
        """
        if not self.config.enabled:
            return

        if level.value < self.config.level.value:
            return

        # Format message with metadata
        metadata = {**self.config.metadata, **kwargs}
        formatted = f"{level.value.upper()}: {message}"
        if metadata:
            formatted += f" | {metadata}"

        # Write to stderr
        print(formatted, file=sys.stderr)

    def get_stats(self) -> dict[str, Any]:
        """Get logger statistics."""
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "level": self.config.level.value,
            "metadata": self.config.metadata,
        }
