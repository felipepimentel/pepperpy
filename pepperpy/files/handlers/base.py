"""Base file handler implementation"""

from datetime import datetime
from pathlib import Path
from typing import Any, Generic, TypeVar

from ..types import FileMetadata, FileType, PathLike

T = TypeVar("T")


class FileHandler(Generic[T]):
    """Base handler for file operations"""

    def _create_metadata(
        self,
        path: Path,
        file_type: FileType,
        mime_type: str,
        format_str: str,
        metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Create file metadata"""
        return FileMetadata(
            name=path.name,
            size=path.stat().st_size,
            file_type=file_type,
            mime_type=mime_type,
            format=format_str,
            created_at=datetime.fromtimestamp(path.stat().st_ctime),
            modified_at=datetime.fromtimestamp(path.stat().st_mtime),
            path=path,
            metadata=metadata or {},
        )

    def _to_path(self, path: PathLike) -> Path:
        """Convert path-like to Path"""
        return Path(path)
