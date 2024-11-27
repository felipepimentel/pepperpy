"""Logging types"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any


class LogLevel(Enum):
    """Log levels"""

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


@dataclass
class LogRecord:
    """Log record"""

    level: LogLevel
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    logger_name: str = ""
    module: str = ""
    function: str = ""
    line: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
