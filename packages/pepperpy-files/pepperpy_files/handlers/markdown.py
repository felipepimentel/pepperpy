"""Markdown file handler implementation"""

from pathlib import Path
from typing import Any, Dict

from bko.files.exceptions import FileError
from bko.files.handlers.base import BaseFileHandler
from bko.files.types import FileContent, FileMetadata


class MarkdownFileHandler(BaseFileHandler):
    """Handler for markdown file operations"""

    async def initialize(self) -> None:
        """Initialize handler"""
        await super().initialize()
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup handler"""
        await super().cleanup()
        self._initialized = False

    async def read(self, path: Path, **kwargs: Dict[str, Any]) -> FileContent:
        """Read markdown file content"""
        path = self._to_path(path)

        if not path.exists():
            raise FileError(f"File does not exist: {path}")

        if not self._initialized:
            raise RuntimeError("Handler not initialized")

        if path.stat().st_size > self.config.max_file_size:
            raise FileError(f"File too large: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            return FileContent(
                content=content,
                metadata=FileMetadata(
                    name=path.name,
                    mime_type="text/markdown",
                    path=path,
                    type="text",
                    extension=path.suffix,
                    format="utf-8",
                    size=path.stat().st_size,
                ),
            )
        except Exception as e:
            raise FileError(f"Failed to read markdown file: {e}", cause=e)

    async def write(self, path: Path, content: FileContent, **kwargs: Dict[str, Any]) -> None:
        """Write markdown file content"""
        path = self._to_path(path)

        if not self._initialized:
            raise RuntimeError("Handler not initialized")

        if not isinstance(content.content, str):
            raise FileError("Invalid markdown content")

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.content)
        except Exception as e:
            raise FileError(f"Failed to write markdown file: {e}", cause=e)
