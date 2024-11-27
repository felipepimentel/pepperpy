"""Markup file handler implementation"""

from pathlib import Path

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandlerConfig


class MarkupHandler(BaseFileHandler[str]):
    """Handler for markup files"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__(
            config=FileHandlerConfig(
                base_path=Path("."),
                allowed_extensions={".md", ".rst", ".txt", ".html", ".xml"},
                max_file_size=10 * 1024 * 1024,  # 10MB
                metadata={
                    "type": FileType.MARKUP,
                    "mime_type": "text/plain",
                },
            )
        )
        self._initialized = True

    def _to_path(self, file: PathLike) -> Path:
        """Convert PathLike to Path"""
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return f"text/{path.suffix[1:]}"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.MARKUP

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix[1:]

    async def read(self, file: PathLike) -> FileContent[str]:
        """Read markup file"""
        try:
            path = self._to_path(file)
            self._validate_path(path)
            self._validate_size(path)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            metadata = self._create_metadata(
                path=path,
                size=len(content.encode("utf-8")),  # Tamanho em bytes do conteúdo UTF-8
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read markup file: {e}", cause=e)

    async def write(self, content: str, output: PathLike) -> None:
        """Write markup file"""
        try:
            path = self._to_path(output)
            self._validate_path(path.parent)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise FileError(f"Failed to write markup file: {e}", cause=e)

    def _validate_path(self, path: Path) -> None:
        """Validate file path"""
        if not path.exists():
            raise FileError(f"File not found: {path}")
        if not path.is_file():
            raise FileError(f"Not a file: {path}")
        if path.suffix not in self.config.allowed_extensions:
            raise FileError(f"Invalid file extension: {path.suffix}")

    def _validate_size(self, path: Path) -> None:
        """Validate file size"""
        size = path.stat().st_size
        if size > self.config.max_file_size:
            raise FileError(
                f"File size ({size} bytes) exceeds limit ({self.config.max_file_size} bytes)"
            )

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
