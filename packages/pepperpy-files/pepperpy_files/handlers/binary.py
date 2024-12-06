"""Binary file handler implementation"""

from pathlib import Path

from ..base import BaseHandler, FileHandlerConfig
from ..enums import FileType
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class BinaryError(FileError):
    """Binary file specific error"""


class BinaryHandler(BaseHandler):
    """Handler for binary files"""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler

        Args:
            config: Optional handler configuration
        """
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions([".bin", ".dat"]),
                encoding="binary",
                max_file_size=100 * 1024 * 1024,  # 100MB
                metadata={
                    "type": FileType.BINARY,
                    "mime_type": "application/octet-stream",
                },
            )
        )

    async def read(self, path: Path) -> FileContent:
        """Read binary file

        Args:
            path: Path to binary file

        Returns:
            Binary file content

        Raises:
            BinaryError: If file cannot be read
        """
        try:
            if not path.exists():
                raise BinaryError(f"File not found: {path}")

            if not path.is_file():
                raise BinaryError(f"Not a file: {path}")

            size = path.stat().st_size
            if size > self.config.max_file_size:
                raise BinaryError(
                    f"File size ({size} bytes) exceeds limit ({self.config.max_file_size} bytes)"
                )

            content = path.read_bytes()
            metadata = FileMetadata(
                name=path.name,
                mime_type="application/octet-stream",
                size=len(content),
                format=path.suffix.lstrip("."),
            )
            return FileContent(path=path, content=content, metadata=metadata)
        except Exception as e:
            raise BinaryError(f"Failed to read binary file: {e}") from e

    async def write(self, content: FileContent, path: Path | None = None) -> None:
        """Write binary file

        Args:
            content: Binary content to write
            path: Optional path to write to

        Raises:
            BinaryError: If file cannot be written
        """
        try:
            target = path or content.path
            if isinstance(content.content, bytes):
                target.write_bytes(content.content)
            else:
                raise BinaryError("Content must be bytes")
        except Exception as e:
            raise BinaryError(f"Failed to write binary file: {e}") from e
