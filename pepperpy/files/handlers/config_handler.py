"""Configuration file handler implementation"""

from pathlib import Path
from typing import Any, Dict, Optional

import tomli
import tomli_w
from jsonschema import ValidationError, validate

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class ConfigHandler(BaseHandler):
    """Handler for configuration files"""

    def __init__(self):
        super().__init__()
        self._schema: Optional[Dict[str, Any]] = None

    async def read(self, path: Path) -> FileContent:
        """Read configuration file"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            # Parse config based on extension
            if path.suffix == ".toml":
                data = tomli.loads(content)
            else:
                raise FileError(f"Unsupported config format: {path.suffix}")

            # Validate against schema if available
            if self._schema is not None:
                try:
                    validate(instance=data, schema=self._schema)
                except ValidationError as e:
                    raise FileError(f"Config validation failed: {str(e)}")

            return FileContent(content=data, metadata=metadata.metadata, format="config")
        except Exception as e:
            raise FileError(f"Failed to read config file: {str(e)}", cause=e)

    async def write(
        self,
        path: Path,
        content: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> FileMetadata:
        """Write configuration file"""
        try:
            # Validate against schema if available
            if self._schema is not None:
                try:
                    validate(instance=content, schema=self._schema)
                except ValidationError as e:
                    raise FileError(f"Config validation failed: {str(e)}")

            # Convert to string based on format
            if path.suffix == ".toml":
                config_content = tomli_w.dumps(content)
            else:
                raise FileError(f"Unsupported config format: {path.suffix}")

            return await self._write_file(path, config_content)
        except Exception as e:
            raise FileError(f"Failed to write config file: {str(e)}", cause=e)

    def set_schema(self, schema: Dict[str, Any]) -> None:
        """Set JSON schema for validation

        Args:
            schema: JSON schema
        """
        self._schema = schema

    def clear_schema(self) -> None:
        """Clear JSON schema"""
        self._schema = None
