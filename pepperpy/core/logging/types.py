"""Logging type definitions"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class LogLevel(Enum):
    """Log levels"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogRecord:
    """Log record data"""
    level: LogLevel
    message: str
    timestamp: datetime
    module: str
    function: str
    line: int
    metadata: dict[str, Any]
