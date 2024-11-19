"""Configuration file handler implementation"""

from pathlib import Path
from typing import Any

import tomli
import tomli_w

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import FileHandler


class ConfigHandler(FileHandler[dict[str, Any]]):
    """Handler for configuration files"""

    async def read(self, path: PathLike) -> FileContent[dict[str, Any]]:
        """Read configuration file"""
        try:
            file_path = self._to_path(path)
            content = await self._read_content(file_path)

            metadata = self._create_metadata(
                path=file_path,
                file_type=FileType.CONFIG,
                mime_type="application/toml",
                format_str="toml",
            )

            return FileContent(content=tomli.loads(content), metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to read config file: {e!s}", cause=e)

    async def write(
        self,
        content: dict[str, Any],
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write configuration file"""
        try:
            file_path = self._to_path(path)

            # Convert to string
            if file_path.suffix == ".toml":
                data = tomli_w.dumps(content)
            else:  # YAML
                data = tomli_w.dumps(content)

            await self._write_text(data, file_path)
            return file_path

        except Exception as e:
            raise FileError(f"Failed to write config file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> str:
        """Read configuration content"""
        return path.read_text()

    async def _write_text(self, content: str, path: Path) -> None:
        """Write text content"""
        path.write_text(content)
