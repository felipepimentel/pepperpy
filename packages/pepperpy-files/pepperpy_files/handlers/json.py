"""JSON file handler implementation"""

import json
from pathlib import Path

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandlerConfig


class JSONFileHandler(BaseFileHandler[dict]):
    """JSON file handler implementation"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__(
            config=FileHandlerConfig(
                base_path=Path("."),
                allowed_extensions={".json"},
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

    def _to_path(self, file: PathLike) -> Path:
        """Convert PathLike to Path"""
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

    async def read(self, file: PathLike) -> FileContent[dict]:
        """Read JSON file"""
        try:
            path = self._to_path(file)
            self._validate_path(path)
            self._validate_size(path)

            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)

            metadata = self._create_metadata(path=path, size=path.stat().st_size)

            return FileContent(content=content, metadata=metadata)
        except json.JSONDecodeError as e:
            raise FileError(f"Invalid JSON: {e}", cause=e)
        except Exception as e:
            raise FileError(f"Failed to read JSON file: {e}", cause=e)

    async def write(self, content: dict, output: PathLike) -> None:
        """Write JSON file"""
        try:
            path = self._to_path(output)
            self._validate_path(path.parent)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=2)
        except json.JSONDecodeError as e:
            raise FileError(f"Invalid JSON: {e}", cause=e)
        except Exception as e:
            raise FileError(f"Failed to write JSON file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
