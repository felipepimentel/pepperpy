"""File manager implementation"""

from pathlib import Path
from typing import Any, Optional, TypeVar

from pepperpy.core.module import BaseModule

from .config import FileManagerConfig
from .exceptions import FileError
from .handlers.base import FileHandler

T = TypeVar("T")


class FileManager(BaseModule[FileManagerConfig]):
    """File manager implementation"""

    def __init__(self, config: Optional[FileManagerConfig] = None) -> None:
        """Initialize manager"""
        super().__init__(config or FileManagerConfig.get_default())
        self._handlers: dict[str, FileHandler[Any]] = {}

    async def _initialize(self) -> None:
        """Initialize manager"""
        # Initialize handlers based on config
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        for handler in self._handlers.values():
            await handler.cleanup()
        self._handlers.clear()

    def register_handler(self, extension: str, handler: FileHandler[Any]) -> None:
        """Register file handler"""
        self._handlers[extension.lower()] = handler

    async def read_file(self, path: Path) -> Any:
        """Read file using appropriate handler"""
        if not self._initialized:
            await self.initialize()

        try:
            extension = path.suffix.lower()
            handler = self._handlers.get(extension)
            if not handler:
                raise FileError(f"No handler found for extension: {extension}")
            return await handler.read(path)
        except Exception as e:
            raise FileError(f"Failed to read file: {e}", cause=e)

    async def write_file(self, content: Any, path: Path) -> None:
        """Write file using appropriate handler"""
        if not self._initialized:
            await self.initialize()

        try:
            extension = path.suffix.lower()
            handler = self._handlers.get(extension)
            if not handler:
                raise FileError(f"No handler found for extension: {extension}")
            await handler.write(content, path)
        except Exception as e:
            raise FileError(f"Failed to write file: {e}", cause=e)
