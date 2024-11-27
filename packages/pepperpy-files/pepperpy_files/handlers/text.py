"""Text file handler implementation"""

from pathlib import Path
from typing import Optional

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandlerConfig


class TextFileHandler(BaseFileHandler[str]):
    """Text file handler implementation"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__(
            config=FileHandlerConfig(
                base_path=Path("."),
                allowed_extensions={".txt", ".log", ".csv", ".tsv"},
                max_file_size=50 * 1024 * 1024,  # 50MB
                metadata={
                    "type": FileType.TEXT,
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
        return "text/plain"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.TEXT

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix[1:]

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

    async def read(self, file: PathLike, encoding: str = "utf-8") -> FileContent[str]:
        """Read text file"""
        try:
            path = self._to_path(file)
            self._validate_path(path)
            self._validate_size(path)

            with open(path, "r", encoding=encoding) as f:
                content = f.read()

            metadata = self._create_metadata(
                path=path,
                size=len(content.encode(encoding)),  # Tamanho em bytes do conteúdo codificado
            )

            return FileContent(content=content, metadata=metadata)
        except UnicodeError as e:
            raise FileError(f"Invalid text encoding: {e}", cause=e)
        except Exception as e:
            raise FileError(f"Failed to read text file: {e}", cause=e)

    async def write(self, content: str, output: PathLike, encoding: Optional[str] = None) -> None:
        """Write text file"""
        try:
            path = self._to_path(output)
            self._validate_path(path.parent)

            file_encoding = encoding or "utf-8"

            with open(path, "w", encoding=file_encoding) as f:
                f.write(content)
        except UnicodeError as e:
            raise FileError(f"Invalid text encoding: {e}", cause=e)
        except Exception as e:
            raise FileError(f"Failed to write text file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
