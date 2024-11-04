import contextvars
import logging
import sys
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Optional

from rich.logging import RichHandler

# Contexto global para logging
context = contextvars.ContextVar("log_context", default={})


class LogFormatter(logging.Formatter):
    """Formatador personalizado para logs"""

    def __init__(self):
        super().__init__()
        self.default_msec_format = "%s.%03d"

    def format(self, record: logging.LogRecord) -> str:
        """Formata registro de log com contexto"""
        # Adiciona contexto ao registro
        ctx = context.get()
        extra = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "logger": record.name,
            "level": record.levelname,
            **ctx,
            **(record.__dict__.get("extra", {})),
        }

        # Formata mensagem
        if isinstance(record.msg, dict):
            message = record.msg
        else:
            message = str(record.msg)

        return f"[{extra['timestamp']}] {record.levelname}: {message}"


class ContextLogger:
    """Logger com suporte a contexto"""

    def __init__(self, name: str, level: int = logging.INFO, rich_output: bool = True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Remove handlers existentes
        self.logger.handlers.clear()

        # Configura handler
        if rich_output:
            handler = RichHandler(rich_tracebacks=True, markup=True, show_time=False)
        else:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(LogFormatter())

        self.logger.addHandler(handler)

    def _log(self, level: int, message: Any, **kwargs: Any) -> None:
        """Método base para logging"""
        extra = kwargs.pop("extra", {})
        if kwargs:
            extra.update(kwargs)

        if isinstance(message, dict):
            message = {**message, **extra}

        self.logger.log(level, message, extra={"extra": extra})

    def debug(self, message: Any, **kwargs: Any) -> None:
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: Any, **kwargs: Any) -> None:
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: Any, **kwargs: Any) -> None:
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: Any, **kwargs: Any) -> None:
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: Any, **kwargs: Any) -> None:
        self._log(logging.CRITICAL, message, **kwargs)

    @contextmanager
    def context(self, **kwargs: Any):
        """Adiciona contexto temporário ao logger"""
        token = context.set({**context.get(), **kwargs})
        try:
            yield self
        finally:
            context.reset(token)

    def bind(self, **kwargs: Any) -> "ContextLogger":
        """Cria nova instância do logger com contexto adicional"""
        new_logger = ContextLogger(self.logger.name)
        new_logger.logger = self.logger
        context.set({**context.get(), **kwargs})
        return new_logger


class LoggerManager:
    """Gerenciador global de loggers"""

    _loggers: Dict[str, ContextLogger] = {}
    _default_level = logging.INFO
    _rich_output = True

    @classmethod
    def get_logger(cls, name: str) -> ContextLogger:
        """Obtém ou cria logger"""
        if name not in cls._loggers:
            cls._loggers[name] = ContextLogger(
                name, level=cls._default_level, rich_output=cls._rich_output
            )
        return cls._loggers[name]

    @classmethod
    def configure(
        cls, level: Optional[int] = None, rich_output: Optional[bool] = None
    ) -> None:
        """Configura comportamento global dos loggers"""
        if level is not None:
            cls._default_level = level
        if rich_output is not None:
            cls._rich_output = rich_output

        # Atualiza loggers existentes
        for logger in cls._loggers.values():
            if level is not None:
                logger.logger.setLevel(level)
            if rich_output is not None:
                logger.logger.handlers.clear()
                handler = (
                    RichHandler(rich_tracebacks=True, markup=True)
                    if rich_output
                    else logging.StreamHandler(sys.stdout)
                )
                if not rich_output:
                    handler.setFormatter(LogFormatter())
                logger.logger.addHandler(handler)


def get_logger(name: str) -> ContextLogger:
    """Função auxiliar para obter logger"""
    return LoggerManager.get_logger(name)
