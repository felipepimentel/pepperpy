"""Markdown file handler implementation"""

from pathlib import Path
from typing import Any, Dict, Optional

from markdown_it import MarkdownIt

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class MarkdownHandler(BaseHandler):
    """Handler for Markdown files"""

    def __init__(self):
        super().__init__()
        self._parser = MarkdownIt()

    async def read(self, path: Path) -> FileContent:
        """Read Markdown file"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            # Parse Markdown content
            html = self._parser.render(content)

            return FileContent(content=html, metadata=metadata.metadata, format="markdown")
        except Exception as e:
            raise FileError(f"Failed to read Markdown file: {str(e)}", cause=e)

    async def write(
        self, path: Path, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> FileMetadata:
        """Write Markdown file"""
        try:
            return await self._write_file(path, content)
        except Exception as e:
            raise FileError(f"Failed to write Markdown file: {str(e)}", cause=e)
