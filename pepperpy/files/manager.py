"""File manager implementation"""

from pathlib import Path
from typing import Any, Generic, Protocol, TypeVar

from pepperpy.core.module import InitializableModule

T = TypeVar("T", covariant=True)


class FileHandler(Protocol[T]):
    """File handler protocol"""

    async def read_file(self, path: str) -> T:
        """Read file content"""
        ...


class FileManager(InitializableModule, Generic[T]):
    """File manager implementation"""

    def __init__(self) -> None:
        super().__init__()
        self._handlers: dict[str, FileHandler[Any]] = {}

    async def _initialize(self) -> None:
        """Initialize file manager"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup file manager"""
        self._handlers.clear()

    def register_handler(self, extension: str, handler: FileHandler[Any]) -> None:
        """Register file handler"""
        self._handlers[extension] = handler

    async def read_file(self, path: str) -> Any:
        """Read file content"""
        ext = Path(path).suffix
        handler = self._handlers.get(ext)
        if not handler:
            raise ValueError(f"No handler for extension: {ext}")
        return await handler.read_file(path)
