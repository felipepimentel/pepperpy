"""Text file handler implementation"""

from pathlib import Path

from ..base import BaseHandler, FileHandlerConfig
from ..enums import FileType
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class TextError(FileError):
    """Text specific error"""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class TextHandler(BaseHandler):
    """Text file handler implementation"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__(
            config=FileHandlerConfig(
                allowed_extensions=self._convert_extensions([".txt", ".md", ".rst"]),
                max_file_size=10 * 1024 * 1024,  # 10MB
                metadata={
                    "type": FileType.TEXT,
                    "mime_type": "text/plain",
                },
            )
        )
        self._initialized = True

    def _to_path(self, file: str | Path) -> Path:
        """Convert to Path object.

        Args:
            file: Path-like object to convert

        Returns:
            Converted Path object
        """
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "text/plain"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.TEXT

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix.lstrip(".")

    def _validate_path(self, path: Path) -> None:
        """Validate file path"""
        if not path.exists():
            raise TextError(f"File not found: {path}")
        if not path.is_file():
            raise TextError(f"Not a file: {path}")
        if path.suffix not in self.config.allowed_extensions:
            raise TextError(f"Invalid file extension: {path.suffix}")

    def _validate_size(self, path: Path) -> None:
        """Validate file size"""
        size = path.stat().st_size
        if size > self.config.max_file_size:
            raise TextError(
                f"File size ({size} bytes) exceeds limit ({self.config.max_file_size} bytes)"
            )

    async def read(self, file: str | Path) -> FileContent:
        """Read text file"""
        try:
            path = self._to_path(file)
            self._validate_path(path)
            self._validate_size(path)

            content = path.read_text(encoding=self.config.encoding)

            file_metadata = FileMetadata(
                name=path.name,
                mime_type=self._get_mime_type(path),
                size=len(content.encode()),
                format=self._get_format(path),
                additional_metadata={},
            )

            return FileContent(path=path, content=content, metadata=file_metadata)
        except Exception as e:
            raise TextError(f"Failed to read text file: {e}", cause=e)

    async def write(self, content: str, output: str | Path) -> None:
        """Write text file"""
        try:
            path = self._to_path(output)
            self._validate_path(path.parent)

            path.write_text(content, encoding=self.config.encoding)
        except Exception as e:
            raise TextError(f"Failed to write text file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
