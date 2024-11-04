import contextvars
import logging
from contextlib import contextmanager

context = contextvars.ContextVar("log_context", default={})


class ContextLogger:
    """Context-aware logger"""

    def __init__(self, name: str) -> None:
        self._logger = logging.getLogger(name)

    def _format_message(self, message: str) -> str:
        ctx = context.get()
        if ctx:
            return f"[{' '.join(f'{k}={v}' for k, v in ctx.items())}] {message}"
        return message

    @contextmanager
    def context(self, **kwargs):
        """Add context to log messages"""
        token = context.set({**context.get(), **kwargs})
        try:
            yield self
        finally:
            context.reset(token)

    def debug(self, message: str, *args, **kwargs) -> None:
        self._logger.debug(self._format_message(message), *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        self._logger.info(self._format_message(message), *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        self._logger.warning(self._format_message(message), *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        self._logger.error(self._format_message(message), *args, **kwargs)
