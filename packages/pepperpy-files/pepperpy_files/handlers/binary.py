"""Binary file handler implementation"""

from pathlib import Path

from bko.files.exceptions import FileError
from bko.files.types import FileContent, FileType, PathLike

from .base import BaseFileHandler


class BinaryFileHandler(BaseFileHandler[bytes]):
    """Binary file handler implementation"""

    def _ensure_initialized(self) -> None:
        """Ensure handler is initialized"""
        if not self._initialized:
            raise RuntimeError("Handler is not initialized")

    def _validate_path(self, path: Path) -> None:
        """Validate file path.

        Args:
            path: Path to validate

        Raises:
            FileError: If path is invalid
        """
        if not path.exists():
            raise FileError(f"File not found: {path}")
        if not path.is_file():
            raise FileError(f"Not a file: {path}")
        if path.suffix not in self.config.allowed_extensions:
            raise FileError(f"Invalid file extension: {path.suffix}")

    def _validate_size(self, path: Path) -> None:
        """Validate file size.

        Args:
            path: Path to validate

        Raises:
            FileError: If file size exceeds limit
        """
        size = path.stat().st_size
        if size > self.config.max_file_size:
            raise FileError(
                f"File size ({size} bytes) exceeds limit ({self.config.max_file_size} bytes)"
            )

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read binary file"""
        self._ensure_initialized()
        try:
            path = Path(file) if isinstance(file, str) else file
            self._validate_path(path)
            self._validate_size(path)

            content = path.read_bytes()
            metadata = self._create_metadata(path=path, size=len(content))
            return FileContent(content=content, metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to read binary file: {e}", cause=e)

    async def write(self, content: bytes, output: PathLike) -> None:
        """Write binary file"""
        self._ensure_initialized()
        try:
            path = Path(output) if isinstance(output, str) else output
            self._validate_path(path.parent)

            if len(content) > self.config.max_file_size:
                raise FileError(
                    f"Content size ({len(content)} bytes) exceeds limit "
                    f"({self.config.max_file_size} bytes)"
                )

            path.write_bytes(content)

        except Exception as e:
            raise FileError(f"Failed to write binary file: {e}", cause=e)

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "application/octet-stream"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.BINARY

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return "binary"
