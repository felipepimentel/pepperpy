"""Logging handlers"""

import sys
from typing import TextIO

from rich.console import Console

from .exceptions import LogHandlerError
from .types import LogLevel, LogRecord


class BaseLogHandler:
    """Base log handler"""

    async def handle(self, record: LogRecord) -> None:
        """Handle log record"""
        try:
            await self.emit(record)
        except Exception as e:
            raise LogHandlerError(f"Failed to handle log record: {e!s}", cause=e)

    async def emit(self, record: LogRecord) -> None:
        """Emit log record"""
        raise NotImplementedError("Async handler not implemented")


class ConsoleLogHandler(BaseLogHandler):
    """Console log handler"""

    def __init__(self, stream: TextIO | None = None) -> None:
        self.console = Console(file=stream or sys.stdout)
        self._styles = {
            LogLevel.DEBUG: "dim",
            LogLevel.INFO: "blue",
            LogLevel.WARNING: "yellow",
            LogLevel.ERROR: "red",
            LogLevel.CRITICAL: "red bold",
        }

    async def emit(self, record: LogRecord) -> None:
        """Emit log record to console"""
        try:
            style = self._styles.get(record.level, "default")

            # Format message
            message = str(record.message)
            if record.metadata:
                metadata_str = " ".join(f"{k}={v}" for k, v in record.metadata.items())
                message = f"{message} ({metadata_str})"

            # Add emoji based on level
            emoji = self._get_level_emoji(record.level)
            if emoji:
                message = f"{emoji} {message}"

            self.console.print(message, style=style)
        except Exception as e:
            raise LogHandlerError(f"Failed to emit log record: {e!s}", cause=e)

    def _get_level_emoji(self, level: LogLevel) -> str:
        """Get emoji for log level"""
        emojis = {
            LogLevel.DEBUG: "🔍",
            LogLevel.INFO: "ℹ️",
            LogLevel.WARNING: "⚠️",
            LogLevel.ERROR: "❌",
            LogLevel.CRITICAL: "🚨",
        }
        return emojis.get(level, "")


class FileLogHandler(BaseLogHandler):
    """File log handler"""

    def __init__(self, filename: str) -> None:
        self.filename = filename

    async def emit(self, record: LogRecord) -> None:
        """Emit log record to file"""
        try:
            # Format message
            message = f"[{record.level.name}] {record.message}"
            if record.metadata:
                metadata_str = " ".join(f"{k}={v}" for k, v in record.metadata.items())
                message = f"{message} ({metadata_str})"

            # Append to file
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(f"{message}\n")
        except Exception as e:
            raise LogHandlerError(f"Failed to emit log record: {e!s}", cause=e)
