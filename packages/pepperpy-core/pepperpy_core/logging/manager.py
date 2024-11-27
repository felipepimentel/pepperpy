"""Logging manager implementation"""

from typing import Any, Optional

from ..base.module import BaseModule
from .base import LogConfig, StructuredLogger


class LogManager(BaseModule[LogConfig]):
    """Logging manager implementation"""

    def __init__(self, config: Optional[LogConfig] = None) -> None:
        super().__init__(config or LogConfig())
        self._loggers: dict[str, StructuredLogger] = {}
        self._default_logger: Optional[StructuredLogger] = None

    async def _initialize(self) -> None:
        """Initialize logging manager"""
        self._loggers.clear()
        self._initialized = True
        self._default_logger = StructuredLogger("default", self.config)

    async def _cleanup(self) -> None:
        """Cleanup logging manager"""
        self._loggers.clear()
        self._default_logger = None

    def get_logger(self, name: str) -> StructuredLogger:
        """Get or create logger"""
        self._ensure_initialized()
        if name not in self._loggers:
            self._loggers[name] = StructuredLogger(name, self.config)
        return self._loggers[name]

    def debug(self, msg: str, **kwargs: Any) -> None:
        """Log debug message"""
        self._ensure_initialized()
        assert self._default_logger is not None
        self._default_logger.debug(msg, **kwargs)

    def info(self, msg: str, **kwargs: Any) -> None:
        """Log info message"""
        self._ensure_initialized()
        assert self._default_logger is not None
        self._default_logger.info(msg, **kwargs)

    def warning(self, msg: str, **kwargs: Any) -> None:
        """Log warning message"""
        self._ensure_initialized()
        assert self._default_logger is not None
        self._default_logger.warning(msg, **kwargs)

    def error(self, msg: str, **kwargs: Any) -> None:
        """Log error message"""
        self._ensure_initialized()
        assert self._default_logger is not None
        self._default_logger.error(msg, **kwargs)
