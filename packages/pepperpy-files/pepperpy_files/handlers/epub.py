"""EPUB file handler."""

import io
from importlib.util import find_spec
from pathlib import Path

# Verificar disponibilidade das dependências opcionais
if not all(map(find_spec, ["ebooklib", "bs4"])):
    raise ImportError(
        "Optional dependencies not found. Please install with: pip install pepperpy-files[epub]"
    )

from ebooklib import epub as epub_module  # type: ignore

from ..base import BaseHandler, FileHandlerConfig
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class EPUBError(FileError):
    """EPUB specific error"""

    def __init__(self, message: str, original_error: Exception | None = None) -> None:
        super().__init__(message)
        self.original_error = original_error


class EPUBHandler(BaseHandler):
    """Handler for EPUB files"""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize EPUB handler.

        Args:
            config: Handler configuration
        """
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions([".epub"]),
                max_file_size=100 * 1024 * 1024,  # 100MB
                metadata={
                    "type": "document",
                    "mime_type": "application/epub+zip",
                },
            )
        )
        self._initialized = False

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "application/epub+zip"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return "document"

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return "epub"

    def _to_path(self, file: str | Path) -> Path:
        """Convert to Path object.

        Args:
            file: Path-like object

        Returns:
            Path object
        """
        return Path(file) if isinstance(file, str) else file

    async def read(self, file: str | Path) -> FileContent:
        """Read EPUB file.

        Args:
            file: Path to EPUB file

        Returns:
            EPUB file content

        Raises:
            EPUBError: If reading fails
        """
        try:
            path = self._to_path(file)

            book = epub_module.read_epub(str(path))

            metadata = {
                "title": book.get_metadata("DC", "title"),
                "creator": book.get_metadata("DC", "creator"),
                "language": book.get_metadata("DC", "language"),
                "identifier": book.get_metadata("DC", "identifier"),
                "rights": book.get_metadata("DC", "rights"),
            }

            with open(path, "rb") as f:
                content = f.read()

            file_metadata = FileMetadata(
                name=path.name,
                mime_type=self._get_mime_type(path),
                size=len(content),
                format=self._get_format(path),
                additional_metadata=metadata,
            )

            return FileContent(path=path, content=content, metadata=file_metadata)

        except Exception as e:
            raise EPUBError(f"Failed to read EPUB file: {str(e)}", original_error=e)

    async def write(self, content: bytes, output: str | Path) -> None:
        """Write EPUB file.

        Args:
            content: EPUB content
            output: Output path

        Raises:
            EPUBError: If writing fails
        """
        try:
            path = self._to_path(output)

            book = epub_module.read_epub(io.BytesIO(content))
            if not book:
                raise EPUBError("Invalid EPUB content")

            with open(path, "wb") as f:
                f.write(content)

        except Exception as e:
            raise EPUBError(f"Failed to write EPUB file: {str(e)}", original_error=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
