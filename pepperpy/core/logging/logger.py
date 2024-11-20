"""Logger implementation"""

import asyncio
import inspect
from typing import Any

from .exceptions import LogError
from .handlers import BaseLogHandler
from .types import LogLevel, LogRecord


class Logger:
    """Async logger implementation"""

    def __init__(self, name: str) -> None:
        self.name = name
        self._handlers: list[BaseLogHandler] = []

    def add_handler(self, handler: BaseLogHandler) -> None:
        """Add log handler"""
        self._handlers.append(handler)

    async def log(self, level: LogLevel, message: str, **metadata: Any) -> None:
        """Log message with level and metadata"""
        try:
            # Get caller info
            frame = inspect.currentframe()
            if frame is not None:
                frame = frame.f_back
            if frame is not None:
                module = frame.f_globals.get("__name__", "")
                function = frame.f_code.co_name
                line = frame.f_lineno
            else:
                module = ""
                function = ""
                line = 0

            record = LogRecord(
                level=level,
                message=message,
                logger_name=self.name,
                module=module,
                function=function,
                line=line,
                metadata=metadata,
            )

            await asyncio.gather(
                *(handler.handle(record) for handler in self._handlers), return_exceptions=True
            )
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


def get_logger(name: str) -> Logger:
    """Get logger instance"""
    return Logger(name)
