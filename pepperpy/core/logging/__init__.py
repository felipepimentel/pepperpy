"""Core logging module"""

from .exceptions import LogError, LogFormatterError, LogHandlerError
from .formatters import JsonFormatter, LogFormatter, TextFormatter
from .handlers import AsyncHandler, FileHandler
from .logger import Logger, get_logger
from .types import LogLevel, LogRecord

__all__ = [
    # Classes base
    "Logger",
    "LogFormatter",
    # Implementações
    "AsyncHandler",
    "FileHandler",
    "JsonFormatter",
    "TextFormatter",
    # Tipos
    "LogLevel",
    "LogRecord",
    # Exceções
    "LogError",
    "LogHandlerError",
    "LogFormatterError",
    # Funções
    "get_logger",
]
