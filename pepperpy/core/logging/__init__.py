"""Core logging module"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Protocol


class Logger(Protocol):
    """Logger protocol defining the interface for logger instances"""

    def debug(self, msg: str, *args, **kwargs) -> None: ...
    def info(self, msg: str, *args, **kwargs) -> None: ...
    def warning(self, msg: str, *args, **kwargs) -> None: ...
    def error(self, msg: str, *args, **kwargs) -> None: ...
    def critical(self, msg: str, *args, **kwargs) -> None: ...


class LogLevel(str, Enum):
    """Log level definitions"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogConfig:
    """Logging configuration"""

    name: str
    level: LogLevel
    console_enabled: bool = True
    colors_enabled: bool = True
    file_path: Optional[str] = None


def get_logger(name: str, config: Optional[LogConfig] = None) -> Logger:
    """Get configured logger instance"""
    import logging
    import sys

    from rich.logging import RichHandler

    logger = logging.getLogger(name)

    if config is None:
        config = LogConfig(name=name, level=LogLevel.INFO)

    logger.setLevel(config.level.value)

    if config.console_enabled:
        console_handler = RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_path=True,
            enable_link_path=True,
            markup=config.colors_enabled,
        )
        console_handler.setLevel(config.level.value)
        logger.addHandler(console_handler)

    if config.file_path:
        file_handler = logging.FileHandler(config.file_path)
        file_handler.setLevel(config.level.value)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)

    if not logger.handlers:
        # Fallback to basic stream handler if no handlers configured
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(handler)

    return logger


__all__ = ["LogLevel", "LogConfig", "get_logger", "Logger"]
