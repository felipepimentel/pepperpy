"""Markdown file handler implementation"""

from pathlib import Path
from typing import Any

import markdown

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike, ensure_path
from .base import FileHandler


class MarkdownHandler(FileHandler[str]):
    """Handler for markdown files"""

    async def read(self, path: PathLike) -> FileContent:
        """Read markdown file"""
        try:
            file_path = ensure_path(path)
            content = await self._read_content(file_path)

            metadata = self._create_metadata(
                path=file_path,
                file_type=FileType.TEXT,
                mime_type="text/markdown",
                format_str="md",
            )

            return FileContent(content=content, metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to read markdown file: {e!s}", cause=e)

    async def write(
        self,
        content: str,
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write markdown file"""
        try:
            file_path = ensure_path(path)
            await self._write_text(content, file_path)
            return file_path
        except Exception as e:
            raise FileError(f"Failed to write markdown file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> str:
        """Read markdown content"""
        return path.read_text()

    async def _write_text(self, content: str, path: Path) -> None:
        """Write text content"""
        path.write_text(content)

    def to_html(self, content: str, **kwargs: Any) -> str:
        """Convert markdown to HTML"""
        return markdown.markdown(content, **kwargs)
