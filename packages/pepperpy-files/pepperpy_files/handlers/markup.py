"""Markup file handler implementation."""

from pathlib import Path

from ..base import BaseHandler, FileHandlerConfig
from ..types import FileMetadata


class MarkupHandler(BaseHandler):
    """Handler for markup files."""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler."""
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions([".txt", ".md", ".rst"]),
                max_file_size=10 * 1024 * 1024,  # 10MB
                metadata={"mime_type": "text/plain"},
            )
        )

    async def _extract_metadata(self, content: str, path: Path) -> FileMetadata:
        """Extract metadata from markup content.

        Args:
            content: Markup content
            path: File path

        Returns:
            File metadata
        """
        return FileMetadata(
            name=path.name,
            mime_type="text/plain",
            size=len(content),
            format=path.suffix.lstrip("."),
        )
