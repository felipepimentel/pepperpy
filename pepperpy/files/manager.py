"""File manager module"""

from pathlib import Path
from typing import Dict, Optional

from pepperpy.files.config import FileHandlerConfig
from pepperpy.files.exceptions import FileError
from pepperpy.files.handlers.base import BaseFileHandler
from pepperpy.files.types import FileContent


class FileManager:
    """File manager implementation"""

    def __init__(self, config: Optional[FileHandlerConfig] = None) -> None:
        """Initialize manager"""
        self.config = config or FileHandlerConfig(
            base_path=Path("."),
            allowed_extensions=set(),
            max_file_size=1024 * 1024 * 10,
            metadata={}
        )
        self._handlers: Dict[str, BaseFileHandler] = {}
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize manager"""
        for handler in self._handlers.values():
            await handler.initialize()
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup manager"""
        for handler in self._handlers.values():
            await handler.cleanup()
        self._initialized = False
        self._handlers.clear()

    def register_handler(self, extension: str, handler: BaseFileHandler) -> None:
        """Register file handler"""
        self._handlers[extension] = handler

    def _get_handler(self, path: Path) -> BaseFileHandler:
        """Get handler for file extension"""
        extension = path.suffix.lower()
        if extension not in self._handlers:
            raise FileError(f"No handler registered for extension: {extension}")
        return self._handlers[extension]

    async def read_file(self, path: Path) -> FileContent:
        """Read file content"""
        if not self._initialized:
            raise RuntimeError("Manager not initialized")

        handler = self._get_handler(path)
        return await handler.read(path)
