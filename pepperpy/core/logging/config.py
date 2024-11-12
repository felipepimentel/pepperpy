"""Logging configuration"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional

from pepperpy.core.config import ModuleConfig


class LogLevel(Enum):
    """Log levels"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogConfig(ModuleConfig):
    """Configuration for logging"""

    name: str
    level: LogLevel = LogLevel.INFO
    console_enabled: bool = True
    file_enabled: bool = False
    file_path: Optional[str] = None
    format: str = "[{timestamp}] {level:<8} {module}: {message}"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    colors_enabled: bool = True
    async_enabled: bool = True
    buffer_size: int = 1000
    metadata: Dict[str, str] = field(default_factory=dict)
