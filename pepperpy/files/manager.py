"""File management implementation for handling file operations."""

from pathlib import Path
from typing import Literal, Union

import aiofiles
from aiofiles.threadpool.binary import AsyncBufferedIOBase
from aiofiles.threadpool.text import AsyncTextIOWrapper

from pepperpy.core.logging import get_logger

from .exceptions import FileError
from .types import PathLike

OpenMode = Literal["r", "w", "a", "x", "rb", "wb", "ab", "xb"]


class FileManager:
    """File manager implementation for handling file operations asynchronously."""

    def __init__(self) -> None:
        """Initialize file manager."""
        self._logger = get_logger(__name__)

    def _to_path(self, path: PathLike) -> Path:
        """Convert path-like object to Path."""
        return Path(path)

    async def write_file(
        self,
        path: PathLike,
        content: Union[str, bytes],
        *,
        mode: OpenMode = "w",
    ) -> None:
        """Write content to file asynchronously."""
        try:
            file_path = self._to_path(path)
            await self._write_async(file_path, content, mode)
        except Exception as e:
            await self._logger.error(f"Failed to write file: {file_path}", error=str(e))
            raise FileError(f"Failed to write file: {e}", cause=e)

    async def _write_async(self, path: Path, content: Union[str, bytes], mode: OpenMode) -> None:
        """Write content to file asynchronously."""
        async with aiofiles.open(path, mode=mode) as file:
            if isinstance(file, AsyncTextIOWrapper):
                await file.write(str(content))
            elif isinstance(file, AsyncBufferedIOBase):
                await file.write(content if isinstance(content, bytes) else str(content).encode())
