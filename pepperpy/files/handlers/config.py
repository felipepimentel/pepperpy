"""Configuration file handler implementation"""

import json
from pathlib import Path

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler


class ConfigHandler(BaseFileHandler[dict]):
    """Handler for configuration files"""

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
        """Read configuration file"""
        try:
            path = self._to_path(file)
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)

            metadata = self._create_metadata(
                path=path,
                size=len(json.dumps(content))  # Usando dumps para obter o tamanho real do JSON
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read config file: {e}", cause=e)

    async def write(self, content: dict, output: PathLike) -> None:
        """Write configuration file"""
        try:
            path = self._to_path(output)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=2)
        except Exception as e:
            raise FileError(f"Failed to write config file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
