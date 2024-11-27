"""Log formatters"""

from abc import ABC, abstractmethod

from .exceptions import LogFormatterError
from .types import LogRecord


class LogFormatter(ABC):
    """Base log formatter"""

    @abstractmethod
    def format(self, record: LogRecord) -> str:
        """Format log record"""
        pass


class JsonFormatter(LogFormatter):
    """JSON log formatter"""

    def format(self, record: LogRecord) -> str:
        """Format log record as JSON"""
        try:
            import json

            return json.dumps(
                {
                    "level": record.level.value,
                    "message": record.message,
                    "timestamp": record.timestamp.isoformat(),
                    "module": record.module,
                    "function": record.function,
                    "line": record.line,
                    "metadata": record.metadata,
                }
            )
        except Exception as e:
            raise LogFormatterError(f"Failed to format log record: {e!s}", cause=e)


class TextFormatter(LogFormatter):
    """Text log formatter"""

    def format(self, record: LogRecord) -> str:
        """Format log record as text"""
        try:
            metadata = " ".join(f"{k}={v}" for k, v in record.metadata.items())
            return (
                f"[{record.timestamp.isoformat()}] {record.level.value}: {record.message} "
                f"({record.module}.{record.function}:{record.line}) {metadata}"
            )
        except Exception as e:
            raise LogFormatterError(f"Failed to format log record: {e!s}", cause=e)
