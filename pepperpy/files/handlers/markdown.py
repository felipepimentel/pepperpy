"""Markdown file handler implementation"""

from pathlib import Path
from typing import Any, Dict, Optional

import markdown

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class MarkdownHandler(BaseHandler):
    """Handler for Markdown files"""

    async def read(self, path: Path) -> FileContent:
        """Read Markdown file"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            # Parse markdown content
            html = markdown.markdown(content, extensions=["meta", "tables", "fenced_code"])

            return FileContent(content=html, metadata=metadata, format="markdown")
        except Exception as e:
            raise FileError(f"Failed to read Markdown file: {str(e)}", cause=e)

    async def write(
        self, path: Path, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> FileMetadata:
        """Write Markdown file"""
        try:
            # Add metadata as YAML front matter if provided
            if metadata:
                yaml_meta = "---\n"
                for key, value in metadata.items():
                    yaml_meta += f"{key}: {value}\n"
                yaml_meta += "---\n\n"
                content = yaml_meta + content

            return await self._write_file(path, content)
        except Exception as e:
            raise FileError(f"Failed to write Markdown file: {str(e)}", cause=e)
