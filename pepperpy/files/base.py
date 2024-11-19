"""Base file handling implementation"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Generic, TypeVar

from .types import FileContent, FileMetadata, FileType, PathLike

T = TypeVar("T")


class BaseHandler(Generic[T], ABC):
    """Base handler implementation"""

    @abstractmethod
    async def read(self, path: PathLike) -> FileContent:
        """Read file content"""
        raise NotImplementedError

    @abstractmethod
    async def write(
        self,
        content: T,
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write file content"""
        raise NotImplementedError

    def _create_metadata(
        self,
        path: Path,
        file_type: FileType,
        mime_type: str,
        format_str: str,
        metadata: dict[str, Any] | None = None,
        media_info: Any | None = None,
        image_info: Any | None = None,
    ) -> FileMetadata:
        """Create file metadata"""
        stat = path.stat()
        return FileMetadata(
            name=path.name,
            size=stat.st_size,
            file_type=file_type,
            mime_type=mime_type,
            format=format_str,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            path=path,
            metadata=metadata or {},
            media_info=media_info,
            image_info=image_info,
        )

    def _to_path(self, path: PathLike) -> Path:
        """Convert path-like to Path"""
        if isinstance(path, Path):
            return path
        if isinstance(path, str):
            return Path(path)
        return Path(str(path))
