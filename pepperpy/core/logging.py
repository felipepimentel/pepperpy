"""Enhanced logging system with structured output and multiple handlers"""

import json
import logging
import logging.handlers
import sys
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import BaseModule, ModuleConfig
from .exceptions import LoggingError
from .types import JsonDict


class LogLevel(Enum):
    """Standard log levels with clear naming"""

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

    @classmethod
    def to_logging_level(cls, level: "LogLevel") -> int:
        """Convert to standard logging level"""
        return {
            cls.DEBUG: logging.DEBUG,
            cls.INFO: logging.INFO,
            cls.WARNING: logging.WARNING,
            cls.ERROR: logging.ERROR,
            cls.CRITICAL: logging.CRITICAL,
        }[level]


@dataclass
class LogContext:
    """Context information for log entries"""

    module: str
    function: Optional[str] = None
    line_number: Optional[int] = None
    thread_id: Optional[int] = field(default_factory=lambda: threading.get_ident())
    timestamp: datetime = field(default_factory=datetime.now)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> JsonDict:
        """Convert context to dictionary"""
        return {
            "module": self.module,
            "function": self.function,
            "line_number": self.line_number,
            "thread_id": self.thread_id,
            "timestamp": self.timestamp.isoformat(),
            **self.extra,
        }


@dataclass
class LoggingConfig(ModuleConfig):
    """Enhanced logging configuration"""

    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[Path] = None
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    json_output: bool = False
    include_context: bool = True
    console_enabled: bool = True
    file_enabled: bool = True
    syslog_enabled: bool = False
    syslog_address: Optional[str] = None
    buffer_capacity: int = 1000
    async_logging: bool = True


class StructuredFormatter(logging.Formatter):
    """Advanced JSON-style structured log formatter"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured data"""
        data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread_id": record.thread,
            "process_id": record.process,
        }

        if hasattr(record, "context"):
            data["context"] = record.context

        if record.exc_info:
            data["exception"] = self.formatException(record.exc_info)

        if record.stack_info:
            data["stack_trace"] = self.formatStack(record.stack_info)

        return json.dumps(data, default=str)


class LoggingModule(BaseModule):
    """Advanced logging system with multiple handlers and async support"""

    __module_name__ = "logging"
    __dependencies__ = ["metrics"]

    def __init__(self, config: Optional[LoggingConfig] = None) -> None:
        super().__init__(config or LoggingConfig())
        self._handlers: Dict[str, logging.Handler] = {}
        self._buffer: List[logging.LogRecord] = []
        self._metrics = None
        self._lock = threading.Lock()

    async def initialize(self) -> None:
        """Initialize logging system"""
        await super().initialize()
        self._metrics = self.get_module("metrics")
        self._configure_root_logger()
        self._setup_handlers()

    async def cleanup(self) -> None:
        """Cleanup logging system"""
        self._flush_buffer()
        for handler in self._handlers.values():
            try:
                handler.close()
            except Exception as e:
                self._logger.error(f"Error closing handler: {e}")
        self._handlers.clear()
        await super().cleanup()

    def _configure_root_logger(self) -> None:
        """Configure root logger settings"""
        root_logger = logging.getLogger()
        root_logger.setLevel(LogLevel.to_logging_level(self.config.level))
        root_logger.handlers.clear()

    def _setup_handlers(self) -> None:
        """Setup configured log handlers"""
        formatter = (
            StructuredFormatter()
            if self.config.json_output
            else logging.Formatter(self.config.format)
        )

        if self.config.console_enabled:
            self._add_console_handler(formatter)

        if self.config.file_enabled and self.config.file_path:
            self._add_file_handler(formatter)

        if self.config.syslog_enabled and self.config.syslog_address:
            self._add_syslog_handler(formatter)

    def _add_console_handler(self, formatter: logging.Formatter) -> None:
        """Add console handler"""
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self._add_handler("console", handler)

    def _add_file_handler(self, formatter: logging.Formatter) -> None:
        """Add rotating file handler"""
        try:
            handler = logging.handlers.RotatingFileHandler(
                self.config.file_path,
                maxBytes=self.config.max_bytes,
                backupCount=self.config.backup_count,
            )
            handler.setFormatter(formatter)
            self._add_handler("file", handler)
        except Exception as e:
            raise LoggingError(f"Failed to setup file handler: {e}") from e

    def _add_syslog_handler(self, formatter: logging.Formatter) -> None:
        """Add syslog handler"""
        try:
            handler = logging.handlers.SysLogHandler(address=self.config.syslog_address)
            handler.setFormatter(formatter)
            self._add_handler("syslog", handler)
        except Exception as e:
            raise LoggingError(f"Failed to setup syslog handler: {e}") from e

    def _add_handler(self, name: str, handler: logging.Handler) -> None:
        """Add handler to root logger"""
        with self._lock:
            self._handlers[name] = handler
            logging.getLogger().addHandler(handler)

    def _flush_buffer(self) -> None:
        """Flush buffered log records"""
        with self._lock:
            for record in self._buffer:
                self._log_record(record)
            self._buffer.clear()

    async def _record_metrics(self, level: str) -> None:
        """Record logging metrics"""
        if self._metrics:
            await self._metrics.record_metric(name="log_entries", value=1, labels={"level": level})
