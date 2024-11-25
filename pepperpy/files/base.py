"""Base file handler implementation"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Generic, TypeVar

from pydantic import BaseModel

from ..core.module import BaseModule
from .config import FileHandlerConfig
from .exceptions import FileError
from .types import FileContent, FileMetadata, FileType, PathLike

T = TypeVar("T", bound=BaseModel)


class BaseFileHandler(Generic[T], BaseModule[FileHandlerConfig], ABC):
    """Base file handler implementation"""

    @abstractmethod
    async def read(self, file: PathLike) -> FileContent[T]:
        """
        Abstract method to read a file.

        Args:
            file (PathLike): Path to the file.

        Returns:
            FileContent[T]: Parsed file content.
        """
        ...

    @abstractmethod
    async def write(self, content: T, output: PathLike) -> None:
        """
        Abstract method to write content to a file.

        Args:
            content (T): Content to be written.
            output (PathLike): Path to the output file.
        """
        ...

    def __init__(self, config: FileHandlerConfig) -> None:
        """
        Initialize handler with configuration.

        Args:
            config (FileHandlerConfig): Configuration for the file handler.
        """
        super().__init__(config)

    def _create_metadata(
        self,
        path: Path,
        file_type: FileType,
        mime_type: str,
        format_str: str,
    ) -> FileMetadata:
        """
        Create metadata for the given file.

        Args:
            path (Path): Path to the file.
            file_type (FileType): Type of the file.
            mime_type (str): MIME type of the file.
            format_str (str): File format string.

        Returns:
            FileMetadata: Metadata for the file.

        Raises:
            FileError: If metadata creation fails.
        """
        try:
            stat = path.stat()
            return FileMetadata(
                path=path,
                size=stat.st_size,
                name=path.name,
                mime_type=mime_type,
                type=file_type,
                extension=path.suffix,
                format=format_str,
                metadata={
                    "created": datetime.fromtimestamp(stat.st_ctime),
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                },
            )
        except Exception as e:
            raise FileError(f"Failed to create metadata: {e}", cause=e)

    def _to_path(self, path: PathLike) -> Path:
        """
        Convert a path-like object to a Path object.

        Args:
            path (PathLike): Path-like object.

        Returns:
            Path: Path object.
        """
        return Path(path) if isinstance(path, str) else path
