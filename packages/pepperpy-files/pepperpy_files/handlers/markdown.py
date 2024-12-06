"""Markdown file handler implementation"""

from pathlib import Path

from ..base import BaseHandler, FileHandlerConfig
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class MarkdownError(FileError):
    """Markdown specific error"""


class MarkdownHandler(BaseHandler):
    """Handler for markdown file operations"""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler.

        Args:
            config: Optional handler configuration
        """
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions([".md", ".markdown"]),
                max_file_size=10 * 1024 * 1024,  # 10MB
                metadata={"mime_type": "text/markdown"},
            )
        )
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize handler"""
        self._initialized = True

    async def read(self, path: Path) -> FileContent:
        """Read markdown file content.

        Args:
            path: Path to markdown file

        Returns:
            Markdown content

        Raises:
            MarkdownError: If file cannot be read
        """
        try:
            if not path.exists():
                raise MarkdownError(f"File does not exist: {path}")

            if not self._initialized:
                raise RuntimeError("Handler not initialized")

            content = path.read_text(encoding=self.config.encoding)
            metadata = FileMetadata(
                name=path.name,
                mime_type="text/markdown",
                size=len(content),
                format=path.suffix.lstrip("."),
            )

            return FileContent(path=path, content=content, metadata=metadata)
        except Exception as e:
            raise MarkdownError(f"Failed to read markdown file: {e}") from e

    async def write(self, content: FileContent, path: Path | None = None) -> None:
        """Write markdown file content.

        Args:
            content: Markdown content to write
            path: Optional path to write to

        Raises:
            MarkdownError: If file cannot be written
        """
        try:
            target = path or content.path
            if not self._initialized:
                raise RuntimeError("Handler not initialized")

            if not isinstance(content.content, str):
                raise MarkdownError("Invalid markdown content - must be string")

            target.write_text(content.content, encoding=self.config.encoding)
        except Exception as e:
            raise MarkdownError(f"Failed to write markdown file: {e}") from e

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self._initialized = False
