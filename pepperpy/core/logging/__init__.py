"""Core logging module"""

import logging
from typing import Optional

from .config import LogConfig, LogLevel
from .logger import Logger


class LoggerAdapter(Logger):
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def debug(self, msg: str, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        self._logger.critical(msg, *args, **kwargs)


def get_logger(name: str, config: Optional[LogConfig] = None) -> Logger:
    """Get configured logger instance"""
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

    return LoggerAdapter(logger)


__all__ = ["LogLevel", "LogConfig", "get_logger", "Logger"]
