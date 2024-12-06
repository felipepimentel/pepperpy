"""Configuration file handler implementation."""

import json
from pathlib import Path
from typing import Any

from ..base import BaseHandler, FileHandlerConfig
from ..enums import FileType
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class ConfigError(FileError):
    """Configuration specific error."""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class ConfigHandler(BaseHandler):
    """Handler for configuration files."""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler."""
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions(
                    [".json", ".yaml", ".yml", ".toml"]
                ),
                max_file_size=10 * 1024 * 1024,  # 10MB
                metadata={"type": FileType.CONFIG, "mime_type": "application/json"},
            )
        )
        self._config: dict[str, Any] = {}

    async def _read_file(self, path: Path) -> str:
        """Read file content.

        Args:
            path: File path

        Returns:
            File content as string

        Raises:
            ConfigError: If file cannot be read
        """
        try:
            with open(path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise ConfigError(f"Failed to read file: {e}", cause=e)

    async def _write_file(self, path: Path, content: str) -> None:
        """Write file content.

        Args:
            path: File path
            content: Content to write

        Raises:
            ConfigError: If file cannot be written
        """
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise ConfigError(f"Failed to write file: {e}", cause=e)

    async def read(self, path: str | Path) -> FileContent:
        """Read configuration file.

        Args:
            path: Path to config file

        Returns:
            Configuration file content

        Raises:
            ConfigError: If file cannot be read
        """
        try:
            path = Path(path)
            if not path.exists():
                raise ConfigError(f"File not found: {path}")

            # Read and parse the config file
            content = await self._read_file(path)
            json_content = json.loads(content)  # Parse JSON string to dict

            # Create metadata
            metadata = FileMetadata(
                name=path.name,
                mime_type="application/json",
                size=len(content),
                format=path.suffix.lstrip("."),
                additional_metadata=json_content,
            )

            # Convert dict to JSON string for storage
            return FileContent(
                path=path,
                content=json.dumps(json_content),  # Convert to string
                metadata=metadata,
            )

        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON: {e}", cause=e)
        except Exception as e:
            raise ConfigError(f"Failed to read config: {e}", cause=e)

    async def write(self, content: dict[str, Any], output: str | Path) -> None:
        """Write configuration file.

        Args:
            content: Configuration content to write
            output: Output path

        Raises:
            ConfigError: If file cannot be written
        """
        try:
            target = Path(output)
            self._config = content

            # Convert to formatted JSON string
            json_str = json.dumps(self._config, indent=2)
            await self._write_file(target, json_str)

        except Exception as e:
            raise ConfigError(f"Failed to save config: {str(e)}") from e

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self._config.clear()
