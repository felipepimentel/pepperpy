"""Base file handling implementation"""

from datetime import datetime
from pathlib import Path
from typing import Any, Protocol, TypeVar

from .types import FileContent, FileMetadata, FileType

T = TypeVar("T")


class FileHandler(Protocol[T]):
    """File handler protocol"""

    async def read(self, file: Path | str) -> FileContent[T]:
        """Read file content"""
        ...

    async def write(self, content: T, output: Path | str) -> None:
        """Write content to file"""
        ...

    async def cleanup(self) -> None:
        """Cleanup resources"""
        ...


class BaseFileHandler:
    """Base file handler implementation"""

    def _to_path(self, file: Path | str) -> Path:
        """Convert to Path object"""
        return file if isinstance(file, Path) else Path(file)

    def _create_metadata(
        self,
        path: Path,
        file_type: FileType,
        mime_type: str,
        format_str: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Create file metadata"""
        stats = path.stat()
        return FileMetadata(
            path=str(path),
            name=path.name,
            extension=path.suffix[1:],
            type=file_type.value,
            mime_type=mime_type,
            format=format_str or path.suffix[1:],
            created_at=datetime.fromtimestamp(stats.st_ctime),
            modified_at=datetime.fromtimestamp(stats.st_mtime),
            size=stats.st_size,
            extra=extra or {},
        )
