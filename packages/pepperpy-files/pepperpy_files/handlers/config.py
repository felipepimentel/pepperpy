"""Configuration file handler implementation."""

from pathlib import Path
from typing import Any, cast

from ..base import BaseHandler, FileHandlerConfig
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class ConfigError(FileError):
    """Configuration specific error."""


class ConfigHandler(BaseHandler):
    """Handler for configuration file operations."""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler.

        Args:
            config: Optional handler configuration
        """
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions(
                    [".json", ".yaml", ".toml", ".ini"]
                ),
                max_file_size=1 * 1024 * 1024,  # 1MB
                metadata={"mime_type": "application/json"},
            )
        )
        self._initialized = False

    async def read(self, path: Path) -> FileContent:
        """Read configuration file content.

        Args:
            path: Path to configuration file

        Returns:
            Configuration content

        Raises:
            ConfigError: If file cannot be read
        """
        try:
            if not path.exists():
                raise ConfigError(f"File does not exist: {path}")

            if not self._initialized:
                raise RuntimeError("Handler not initialized")

            with open(path, encoding="utf-8") as f:
                content = f.read()

            metadata = FileMetadata(
                name=path.name,
                mime_type="application/json",
                size=path.stat().st_size,
                format=path.suffix.lstrip("."),
            )

            return FileContent(path=path, content=content, metadata=metadata)
        except Exception as e:
            raise ConfigError(f"Failed to read configuration file: {e}") from e

    async def write(self, content: FileContent, path: Path | None = None) -> None:
        """Write configuration file content.

        Args:
            content: Configuration content to write
            path: Optional path to write to

        Raises:
            ConfigError: If file cannot be written
        """
        try:
            target = path or content.path
            if not self._initialized:
                raise RuntimeError("Handler not initialized")

            # Handle different content types
            raw_content = content.content
            if isinstance(raw_content, bytes):
                text_content = raw_content.decode("utf-8")
            elif isinstance(raw_content, (bytearray, memoryview)):
                text_content = bytes(raw_content).decode("utf-8")
            else:
                text_content = cast(str, raw_content)

            with open(target, "w", encoding="utf-8") as f:
                f.write(text_content)
        except Exception as e:
            raise ConfigError(f"Failed to write configuration file: {e}") from e

    async def cleanup(self) -> None:
        """Cleanup resources."""
        self._initialized = False

    def _validate_content(self, content: Any) -> None:
        """Validate configuration content."""
        if not isinstance(content, str | bytes):
            raise ValueError("Content must be string or bytes")
