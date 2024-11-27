"""Base logging implementation"""

import logging
import sys
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel

from ..base.types import JsonDict


class LogLevel(str, Enum):
    """Log levels"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def get_logger(name: str, config: Optional["LogConfig"] = None) -> "StructuredLogger":
    """Get structured logger"""
    return StructuredLogger(name, config)


class LogConfig(BaseModel):
    """Logging configuration"""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    handlers: list[str] = ["console", "file"]
    filename: Optional[str] = None
    metadata: JsonDict = {}


class StructuredLogger:
    """Structured logger implementation"""

    def __init__(self, name: str, config: Optional[LogConfig] = None) -> None:
        self.logger = logging.getLogger(name)
        self.config = config or LogConfig()
        self._configure()

    def _configure(self) -> None:
        """Configure logger"""
        self.logger.setLevel(self.config.level)
        formatter = logging.Formatter(fmt=self.config.format, datefmt=self.config.date_format)

        if "console" in self.config.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if "file" in self.config.handlers and self.config.filename:
            file_handler = logging.FileHandler(self.config.filename)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, msg: str, **kwargs: Any) -> None:
        """Log info message"""
        self.logger.info(msg, extra=kwargs)

    def error(self, msg: str, **kwargs: Any) -> None:
        """Log error message"""
        self.logger.error(msg, extra=kwargs)

    def warning(self, msg: str, **kwargs: Any) -> None:
        """Log warning message"""
        self.logger.warning(msg, extra=kwargs)

    def debug(self, msg: str, **kwargs: Any) -> None:
        """Log debug message"""
        self.logger.debug(msg, extra=kwargs)


__all__ = [
    "LogConfig",
    "LogLevel",
    "StructuredLogger",
    "get_logger",
]
