"""Base file handler module"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Generic, TypeVar

from bko.files.config import FileHandlerConfig
from bko.files.types import FileContent, FileMetadata

T = TypeVar("T")  # Type for file content


class BaseFileHandler(ABC, Generic[T]):
    """Base class for file handlers"""

    def __init__(self, config: FileHandlerConfig) -> None:
        """Initialize handler"""
        self.config = config
        self._initialized = False

    def _to_path(self, path: Path) -> Path:
        """Convert path to absolute path"""
        return path if path.is_absolute() else self.config.base_path / path

    def _create_metadata(self, path: Path, size: int) -> FileMetadata:
        """Create file metadata"""
        return FileMetadata(
            name=path.name,
            mime_type=self._get_mime_type(path),
            path=path,
            type=self._get_file_type(path),
            extension=path.suffix,
            format=self._get_format(path),
            size=size,
        )

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "application/octet-stream"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return "binary"

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix.lstrip(".")

    @abstractmethod
    async def read(self, path: Path, **kwargs: Dict[str, Any]) -> FileContent[T]:
        """Read file content"""
        raise NotImplementedError

    @abstractmethod
    async def write(self, path: Path, content: FileContent[T], **kwargs: Dict[str, Any]) -> None:
        """Write file content"""
        raise NotImplementedError

    async def initialize(self) -> None:
        """Initialize handler"""
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup handler"""
        self._initialized = False
