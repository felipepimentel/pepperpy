"""Logger implementation"""

import asyncio
import sys
from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, Optional, Union

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import LogConfig, LogLevel
from .exceptions import LoggingError
from .formatters import LogFormatter
from .handlers import ConsoleHandler, FileHandler


class Logger(BaseModule):
    """Core logger implementation"""

    def __init__(self, name: str, config: Optional[LogConfig] = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="logger",
            version="1.0.0",
            description=f"Logger for {name}",
            dependencies=[],
            config=asdict(config) if config else {},
        )
        self._name = name
        self._handlers = []
        self._formatter = None
        self._queue = asyncio.Queue()
        self._worker = None
        self._running = False

    async def _setup(self) -> None:
        """Initialize logger"""
        try:
            config_dict = self.config
            # Setup formatter
            self._formatter = LogFormatter(
                fmt=config_dict.get("format"),
                date_fmt=config_dict.get("date_format"),
                colors=config_dict.get("colors_enabled", True),
            )

            # Setup handlers
            if config_dict.get("console_enabled", True):
                self._handlers.append(ConsoleHandler(self._formatter))

            if config_dict.get("file_enabled", False):
                file_path = config_dict.get("file_path")
                if not file_path:
                    raise LoggingError("File path not configured for file handler")
                self._handlers.append(FileHandler(self._formatter, file_path))

            # Start async worker if enabled
            if config_dict.get("async_enabled", True):
                self._running = True
                self._worker = asyncio.create_task(self._process_queue())

        except Exception as e:
            raise LoggingError(f"Failed to initialize logger: {str(e)}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup logger resources"""
        self._running = False
        if self._worker:
            self._worker.cancel()
            try:
                await self._worker
            except asyncio.CancelledError:
                pass

        # Cleanup handlers
        for handler in self._handlers:
            await handler.cleanup()

    async def _process_queue(self) -> None:
        """Process log queue"""
        while self._running:
            try:
                record = await self._queue.get()
                for handler in self._handlers:
                    await handler.emit(record)
                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error processing log queue: {str(e)}", file=sys.stderr)

    async def log(self, level: Union[LogLevel, str], message: str, **kwargs: Any) -> None:
        """Log a message"""
        if isinstance(level, str):
            try:
                level = LogLevel[level.upper()]
            except KeyError:
                level = LogLevel.INFO

        record = {
            "timestamp": datetime.now(),
            "level": level.value,
            "module": self._name,
            "message": message,
            "metadata": {**self.config.get("metadata", {}), **kwargs},
        }

        if self.config.get("async_enabled", True):
            await self._queue.put(record)
        else:
            for handler in self._handlers:
                await handler.emit(record)

    async def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message"""
        await self.log(LogLevel.DEBUG, message, **kwargs)

    async def info(self, message: str, **kwargs: Any) -> None:
        """Log info message"""
        await self.log(LogLevel.INFO, message, **kwargs)

    async def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message"""
        await self.log(LogLevel.WARNING, message, **kwargs)

    async def error(self, message: str, **kwargs: Any) -> None:
        """Log error message"""
        await self.log(LogLevel.ERROR, message, **kwargs)

    async def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message"""
        await self.log(LogLevel.CRITICAL, message, **kwargs)


_loggers: Dict[str, Logger] = {}


def get_logger(name: str, config: Optional[LogConfig] = None) -> Logger:
    """Get or create a logger instance"""
    if name not in _loggers:
        _loggers[name] = Logger(name, config)
    return _loggers[name]
