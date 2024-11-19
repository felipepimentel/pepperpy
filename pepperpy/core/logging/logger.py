"""Logging utilities"""

import asyncio
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from .exceptions import LogError
from .formatters import JsonFormatter
from .handlers import AsyncHandler
from .types import LogLevel, LogRecord


@dataclass
class Logger:
    """Logger implementation"""

    name: str
    handlers: list[AsyncHandler]
    formatter: JsonFormatter = JsonFormatter()
    async_: bool = True

    async def log(self, level: LogLevel, message: str, **metadata: Any) -> None:
        """Log a message"""
        try:
            # Criar record
            record = LogRecord(
                level=level,
                message=message,
                timestamp=datetime.now(),
                module=self.name,
                function="",
                line=0,
                metadata=metadata,
            )

            # Converter para dict antes de passar para os handlers
            record_dict = asdict(record)

            if self.async_:
                await asyncio.gather(
                    *(handler.handle(record_dict) for handler in self.handlers)
                )
            else:
                for handler in self.handlers:
                    await handler.handle(record_dict)

        except Exception as e:
            raise LogError(f"Failed to log message: {e!s}", cause=e)

    async def debug(self, message: str, **metadata: Any) -> None:
        """Log debug message"""
        await self.log(LogLevel.DEBUG, message, **metadata)

    async def info(self, message: str, **metadata: Any) -> None:
        """Log info message"""
        await self.log(LogLevel.INFO, message, **metadata)

    async def warning(self, message: str, **metadata: Any) -> None:
        """Log warning message"""
        await self.log(LogLevel.WARNING, message, **metadata)

    async def error(self, message: str, **metadata: Any) -> None:
        """Log error message"""
        await self.log(LogLevel.ERROR, message, **metadata)

    async def critical(self, message: str, **metadata: Any) -> None:
        """Log critical message"""
        await self.log(LogLevel.CRITICAL, message, **metadata)


_loggers: dict[str, Logger] = {}


def get_logger(name: str, async_: bool = True) -> Logger:
    """Get or create logger"""
    if name not in _loggers:
        _loggers[name] = Logger(
            name=name,
            handlers=[AsyncHandler()],
            async_=async_,
        )
    return _loggers[name]
