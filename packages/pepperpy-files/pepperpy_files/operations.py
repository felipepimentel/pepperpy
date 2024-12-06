"""File operations module"""

from pathlib import Path
from typing import Any

from .exceptions import FileError
from .handlers.base import BaseHandler
from .types import FileContent


class FileOperations:
    """File operations handler"""

    def __init__(self) -> None:
        """Initialize file operations"""
        self._handlers: dict[str, BaseHandler] = {}
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize file operations"""
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup file operations"""
        self._initialized = False
        self._handlers.clear()

    def register_handler(self, extension: str, handler: BaseHandler) -> None:
        """Register file handler for extension"""
        self._handlers[extension] = handler

    async def read(self, path: Path, **kwargs: Any) -> FileContent:
        """Read file content using appropriate handler"""
        if not self._initialized:
            raise RuntimeError("File operations not initialized")

        if not path.exists():
            raise FileError(f"File does not exist: {path}")

        handler = self._get_handler(path)
        return await handler.read(path, **kwargs)

    async def write(self, path: Path, content: FileContent, **kwargs: Any) -> None:
        """Write file content using appropriate handler"""
        if not self._initialized:
            raise RuntimeError("File operations not initialized")

        handler = self._get_handler(path)
        await handler.write(content, path, **kwargs)

    def _get_handler(self, path: Path) -> BaseHandler:
        """Get appropriate handler for file"""
        extension = path.suffix.lower()
        handler = self._handlers.get(extension)
        if not handler:
            raise FileError(f"No handler registered for extension: {extension}")
        return handler
