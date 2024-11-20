"""Logging configuration"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from pepperpy.core.types import JsonDict, ModuleConfig


class LogLevel(str, Enum):
    """Log levels"""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogFormat(str, Enum):
    """Log formats"""

    TEXT = "text"
    JSON = "json"
    RICH = "rich"


@dataclass
class LogHandlerConfig:
    """Log handler configuration"""

    name: str
    type: str
    enabled: bool = True
    level: LogLevel = LogLevel.INFO
    format: LogFormat = LogFormat.TEXT
    file_path: Path | None = None
    rotation: bool = False
    max_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class LoggerConfig(ModuleConfig):
    """Logger configuration"""

    name: str
    level: LogLevel = LogLevel.INFO
    handlers: list[LogHandlerConfig] = field(default_factory=list)
    enabled: bool = True
    propagate: bool = True
    capture_warnings: bool = True
    metadata: JsonDict = field(default_factory=dict)
