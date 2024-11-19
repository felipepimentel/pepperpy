"""Configuration file handler implementation"""

from pathlib import Path
from typing import Any

import tomli
import tomli_w
from jsonschema import ValidationError, validate

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike, ensure_path
from .base import FileHandler


class ConfigHandler(FileHandler[dict[str, Any]]):
    """Handler for configuration files"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__()
        self._schema: dict[str, Any] | None = None

    async def read(self, path: PathLike) -> FileContent:
        """Read configuration file"""
        try:
            file_path = ensure_path(path)
            content = await self._read_content(file_path)

            # Parse config based on extension
            if file_path.suffix == ".toml":
                data = tomli.loads(content)
            else:
                raise FileError(f"Unsupported config format: {file_path.suffix}")

            # Validate against schema if available
            if self._schema is not None:
                try:
                    validate(instance=data, schema=self._schema)
                except ValidationError as e:
                    raise FileError(f"Config validation failed: {e!s}")

            metadata = self._create_metadata(
                path=file_path,
                file_type=FileType.CONFIG,
                mime_type="application/toml",
                format_str="toml",
                metadata={"schema": self._schema} if self._schema else {},
            )

            return FileContent(content=data, metadata=metadata)

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
            file_path = ensure_path(path)

            # Validate against schema if available
            if self._schema is not None:
                try:
                    validate(instance=content, schema=self._schema)
                except ValidationError as e:
                    raise FileError(f"Config validation failed: {e!s}")

            # Convert to string based on format
            if file_path.suffix == ".toml":
                config_str = tomli_w.dumps(content)
            else:
                raise FileError(f"Unsupported config format: {file_path.suffix}")

            await self._write_text(config_str, file_path)
            return file_path

        except Exception as e:
            raise FileError(f"Failed to write config file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> str:
        """Read configuration content"""
        return path.read_text()

    async def _write_text(self, content: str, path: Path) -> None:
        """Write text content"""
        path.write_text(content)

    def set_schema(self, schema: dict[str, Any]) -> None:
        """
        Set JSON schema for validation

        Args:
            schema: JSON schema
        """
        self._schema = schema

    def clear_schema(self) -> None:
        """Clear JSON schema"""
        self._schema = None
