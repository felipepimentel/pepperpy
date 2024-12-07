"""YAML file handler implementation."""

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import yaml
from yaml.error import YAMLError

from ..base import BaseHandler
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class YAMLHandler(BaseHandler):
    """YAML file handler implementation."""

    async def read(self, path: Path) -> FileContent:
        """Read YAML file.

        Args:
            path: File path

        Returns:
            File content

        Raises:
            FileError: If file cannot be read
        """
        try:
            with open(path) as f:
                content = yaml.safe_load(f)

            # Convert YAML content to string representation
            content_str = yaml.safe_dump(content) if content is not None else ""
            # Ensure content is str
            if not isinstance(content_str, str):
                content_str = str(content_str)

            return FileContent(
                path=path,
                content=content_str,
                metadata=FileMetadata(
                    name=path.name,
                    mime_type="application/x-yaml",
                    size=path.stat().st_size,
                    format="yaml",
                    additional_metadata=content if isinstance(content, dict) else {},
                ),
            )
        except (OSError, YAMLError) as e:
            raise FileError(f"Failed to read YAML file: {e}") from e

    async def write(self, path: Path, content: Any) -> None:
        """Write YAML file.

        Args:
            path: File path
            content: File content

        Raises:
            FileError: If file cannot be written
        """
        try:
            with open(path, "w") as f:
                yaml.safe_dump(content, f)
        except (OSError, YAMLError) as e:
            raise FileError(f"Failed to write YAML file: {e}") from e

    async def stream(self, path: Path) -> AsyncGenerator[Any, None]:
        """Stream YAML file.

        Args:
            path: File path

        Yields:
            File content chunks

        Raises:
            FileError: If file cannot be streamed
        """
        try:
            with open(path) as f:
                for document in yaml.safe_load_all(f):
                    yield document
        except (OSError, YAMLError) as e:
            raise FileError(f"Failed to stream YAML file: {e}") from e
