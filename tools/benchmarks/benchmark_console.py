"""Benchmark module for console components."""

import importlib.util
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from .base import BenchmarkBase


# Definições de protocolo para type checking
@runtime_checkable
class ConsoleComponentProto(Protocol):
    """Protocol for console components."""

    pass


@runtime_checkable
class ConsoleMessageProto(Protocol):
    """Protocol for console messages."""

    pass


# Verificar disponibilidade do módulo
HAS_CONSOLE = bool(importlib.util.find_spec("pepperpy_console"))

# Definições de tipo
if TYPE_CHECKING:
    pass


class ConsoleBenchmark(BenchmarkBase):
    """Benchmark for console components."""

    def __init__(self) -> None:
        """Initialize benchmark."""
        if not HAS_CONSOLE:
            raise ImportError(
                "Console module not available. Please install pepperpy-console package."
            )
        super().__init__()
