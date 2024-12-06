"""JSON file handler implementation"""

import json
from pathlib import Path

from ..base import BaseHandler, FileHandlerConfig
from ..enums import FileType
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class JSONError(FileError):
    """JSON specific error"""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class JSONHandler(BaseHandler):
    """JSON file handler implementation"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__(
            config=FileHandlerConfig(
                allowed_extensions=self._convert_extensions([".json"]),
                max_file_size=10 * 1024 * 1024,  # 10MB
                metadata={
                    "type": FileType.CONFIG,
                    "mime_type": "application/json",
                },
            )
        )
        self._initialized = True  # Inicializado após configuração

    def _validate_path(self, path: Path) -> None:
        """Validate file path"""
        if not path.exists():
            raise JSONError(f"File not found: {path}")
        if not path.is_file():
            raise JSONError(f"Not a file: {path}")
        if path.suffix not in self.config.allowed_extensions:
            raise JSONError(f"Invalid file extension: {path.suffix}")

    def _validate_size(self, path: Path) -> None:
        """Validate file size"""
        size = path.stat().st_size
        if size > self.config.max_file_size:
            raise JSONError(
                f"File size ({size} bytes) exceeds limit ({self.config.max_file_size} bytes)"
            )

    def _to_path(self, file: str | Path) -> Path:
        """Convert to Path object.

        Args:
            file: Path-like object

        Returns:
            Path object
        """
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "application/json"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.CONFIG

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return "json"

    async def read(self, file: str | Path) -> FileContent:
        """Read JSON file"""
        try:
            path = self._to_path(file)
            self._validate_path(path)
            self._validate_size(path)

            with open(path, encoding="utf-8") as f:
                content = json.load(f)

            file_metadata = FileMetadata(
                name=path.name,
                mime_type=self._get_mime_type(path),
                size=path.stat().st_size,
                format=self._get_format(path),
                additional_metadata=content,
            )

            return FileContent(path=path, content=content, metadata=file_metadata)
        except json.JSONDecodeError as e:
            raise JSONError(f"Invalid JSON: {e}", cause=e)
        except Exception as e:
            raise JSONError(f"Failed to read JSON file: {e}", cause=e)

    async def write(self, content: dict, output: str | Path) -> None:
        """Write JSON file"""
        try:
            path = self._to_path(output)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=2)
        except json.JSONDecodeError as e:
            raise JSONError(f"Invalid JSON: {e}", cause=e)
        except Exception as e:
            raise JSONError(f"Failed to write JSON file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
