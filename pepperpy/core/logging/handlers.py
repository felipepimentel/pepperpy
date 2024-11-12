"""Log handlers implementation"""

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from .exceptions import HandlerError
from .formatters import LogFormatter


class BaseHandler(ABC):
    """Base class for log handlers"""

    def __init__(self, formatter: LogFormatter):
        self.formatter = formatter

    @abstractmethod
    async def emit(self, record: Dict[str, Any]) -> None:
        """Emit log record"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup handler resources"""
        pass


class ConsoleHandler(BaseHandler):
    """Handler for console output"""

    async def emit(self, record: Dict[str, Any]) -> None:
        """Emit log record to console"""
        try:
            message = self.formatter.format(record)
            print(message, file=sys.stdout)
            sys.stdout.flush()
        except Exception as e:
            raise HandlerError(f"Failed to emit console log: {str(e)}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup console handler"""
        sys.stdout.flush()


class FileHandler(BaseHandler):
    """Handler for file output"""

    def __init__(self, formatter: LogFormatter, file_path: str):
        super().__init__(formatter)
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    async def emit(self, record: Dict[str, Any]) -> None:
        """Emit log record to file"""
        try:
            message = self.formatter.format(record)
            with self.file_path.open("a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            raise HandlerError(f"Failed to emit file log: {str(e)}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup file handler"""
        pass  # File is closed after each write
