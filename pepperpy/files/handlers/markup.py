"""Markup file handler implementation"""

from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import FileHandler


class MarkupHandler(FileHandler[str]):
    """Handler for markup files (HTML/XML)"""

    async def read(self, path: PathLike) -> FileContent:
        """Read markup file"""
        try:
            file_path = self._to_path(path)
            content = await self._read_content(file_path)
            if isinstance(content, bytes):
                content = content.decode()

            metadata = self._create_metadata(
                path=file_path,
                file_type=FileType.MARKUP,
                mime_type="text/html" if file_path.suffix == ".html" else "text/xml",
                format_str="html" if file_path.suffix == ".html" else "xml",
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read markup file: {e!s}", cause=e)

    async def write(
        self,
        content: str,
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write markup file"""
        try:
            file_path = self._to_path(path)
            await self._write_text(content, file_path)
            return file_path
        except Exception as e:
            raise FileError(f"Failed to write markup file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> str:
        """Read markup content"""
        return path.read_text()

    async def _write_text(self, content: str, path: Path) -> None:
        """Write text content"""
        path.write_text(content)

    def parse(self, content: str) -> BeautifulSoup:
        """Parse markup content"""
        return BeautifulSoup(content, "html.parser")
