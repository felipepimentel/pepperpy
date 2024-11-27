"""PDF file handler implementation"""

from pathlib import Path

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandlerConfig


class PDFFileHandler(BaseFileHandler[bytes]):
    """PDF file handler implementation"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__(
            config=FileHandlerConfig(
                base_path=Path("."),
                allowed_extensions={".pdf"},
                max_file_size=100 * 1024 * 1024,  # 100MB
                metadata={
                    "type": FileType.DOCUMENT,
                    "mime_type": "application/pdf",
                },
            )
        )
        self._initialized = True

    def _to_path(self, file: PathLike) -> Path:
        """Convert PathLike to Path"""
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "application/pdf"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.DOCUMENT

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return "pdf"

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

    def _validate_pdf_content(self, content: bytes) -> None:
        """Validate PDF content"""
        if not content.startswith(b"%PDF-"):
            raise FileError("Invalid PDF content")

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read PDF file"""
        try:
            path = self._to_path(file)
            self._validate_path(path)
            self._validate_size(path)

            with open(path, "rb") as f:
                content = f.read()

            self._validate_pdf_content(content)

            metadata = self._create_metadata(path=path, size=len(content))

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read PDF file: {e}", cause=e)

    async def write(self, content: bytes, output: PathLike) -> None:
        """Write PDF file"""
        try:
            path = self._to_path(output)
            self._validate_path(path.parent)
            self._validate_pdf_content(content)

            with open(path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise FileError(f"Failed to write PDF file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
