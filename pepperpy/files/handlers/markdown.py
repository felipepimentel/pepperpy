"""Markdown file handler implementation"""

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class MarkdownHandler(BaseFileHandler, FileHandler[str]):
    """Handler for Markdown files"""

    async def read(self, file: PathLike) -> FileContent[str]:
        """Read Markdown file"""
        try:
            path = self._to_path(file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.TEXT,
                mime_type="text/markdown",
                format_str="md",
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read Markdown file: {e}", cause=e)

    async def write(self, content: str, output: PathLike) -> None:
        """Write Markdown file"""
        try:
            path = self._to_path(output)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise FileError(f"Failed to write Markdown file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
