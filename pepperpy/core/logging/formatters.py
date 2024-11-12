"""Log formatters implementation"""

from datetime import datetime
from typing import Any, Dict, Optional

from .exceptions import FormatterError


class LogFormatter:
    """Formatter for log records"""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",
    }

    def __init__(
        self, fmt: Optional[str] = None, date_fmt: Optional[str] = None, colors: bool = True
    ):
        self.fmt = fmt or "[{timestamp}] {level:<8} {module}: {message}"
        self.date_fmt = date_fmt or "%Y-%m-%d %H:%M:%S"
        self.colors = colors

    def format(self, record: Dict[str, Any]) -> str:
        """Format log record"""
        try:
            # Format timestamp
            if isinstance(record["timestamp"], datetime):
                timestamp = record["timestamp"].strftime(self.date_fmt)
            else:
                timestamp = str(record["timestamp"])

            # Apply colors if enabled
            level = record["level"]
            if self.colors:
                level = f"{self.COLORS.get(level, '')}{level}{self.COLORS['RESET']}"

            # Format message with metadata
            message = record["message"]
            if record.get("metadata"):
                metadata_str = " ".join(f"{k}={v}" for k, v in record["metadata"].items())
                message = f"{message} [{metadata_str}]"

            # Format final message
            return self.fmt.format(
                timestamp=timestamp, level=level, module=record["module"], message=message
            )

        except Exception as e:
            raise FormatterError(f"Failed to format log record: {str(e)}", cause=e)
