"""Configuration file handler implementation"""

import json

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class ConfigHandler(BaseFileHandler, FileHandler[dict]):
    """Handler for configuration files"""

    async def read(self, file: PathLike) -> FileContent[dict]:
        """Read configuration file"""
        try:
            path = self._to_path(file)
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.CONFIG,
                mime_type="application/json",
                format_str="json",
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
