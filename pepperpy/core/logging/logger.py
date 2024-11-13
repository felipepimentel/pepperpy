"""Logging utilities"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Protocol

from .exceptions import LoggingError
from .formatters import JsonFormatter
from .handlers import AsyncHandler


@dataclass
class LogRecord:
    """Log record data"""

    level: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class LogHandler(Protocol):
    """Log handler protocol"""

    async def handle(self, record: Dict[str, Any]) -> None: ...


class Logger:
    """Async logger implementation"""

    def __init__(self, name: str):
        self.name = name
        self._handlers: List[LogHandler] = []
        self._formatter = JsonFormatter()

    def add_handler(self, handler: LogHandler) -> None:
        """Add log handler"""
        self._handlers.append(handler)

    async def log(self, level: str, message: str, **metadata: Any) -> None:
        """Log message with metadata"""
        try:
            record = LogRecord(level=level, message=message, metadata=metadata)
            record_dict = {
                "level": record.level,
                "message": record.message,
                "timestamp": record.timestamp.isoformat(),
                **record.metadata,
            }
            await asyncio.gather(*(handler.handle(record_dict) for handler in self._handlers))
        except Exception as e:
            raise LoggingError(f"Failed to log message: {str(e)}", cause=e)

    async def debug(self, message: str, **metadata: Any) -> None:
        """Log debug message"""
        await self.log("DEBUG", message, **metadata)

    async def info(self, message: str, **metadata: Any) -> None:
        """Log info message"""
        await self.log("INFO", message, **metadata)

    async def warning(self, message: str, **metadata: Any) -> None:
        """Log warning message"""
        await self.log("WARNING", message, **metadata)

    async def error(self, message: str, **metadata: Any) -> None:
        """Log error message"""
        await self.log("ERROR", message, **metadata)

    async def critical(self, message: str, **metadata: Any) -> None:
        """Log critical message"""
        await self.log("CRITICAL", message, **metadata)


_loggers: Dict[str, Logger] = {}


def get_logger(name: str) -> Logger:
    """Get or create logger by name"""
    if name not in _loggers:
        logger = Logger(name)
        logger.add_handler(AsyncHandler())
        _loggers[name] = logger
    return _loggers[name]
