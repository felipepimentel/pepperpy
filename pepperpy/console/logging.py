import logging
from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.logging import RichHandler


class ConsoleLogger:
    """Enhanced logging for console module"""

    def __init__(
        self,
        console: Console,
        level: int = logging.INFO,
        log_file: Optional[str] = None,
    ):
        self.console = console

        # Configure rich handler
        rich_handler = RichHandler(console=console, show_time=True, show_path=False)

        # Configure file handler if needed
        handlers = [rich_handler]
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            handlers.append(file_handler)

        # Setup logger
        self.logger = logging.getLogger("console")
        self.logger.setLevel(level)
        for handler in handlers:
            self.logger.addHandler(handler)

    def _format_message(self, message: str, **kwargs: Any) -> str:
        """Format log message with context"""
        if kwargs:
            context = " ".join(f"{k}={v}" for k, v in kwargs.items())
            return f"{message} [{context}]"
        return message

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message"""
        self.logger.debug(self._format_message(message, **kwargs))

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message"""
        self.logger.info(self._format_message(message, **kwargs))

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message"""
        self.logger.warning(self._format_message(message, **kwargs))

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message"""
        self.logger.error(self._format_message(message, **kwargs))

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log exception with traceback"""
        self.logger.exception(self._format_message(message, **kwargs))
