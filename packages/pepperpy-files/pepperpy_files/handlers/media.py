"""Media file handler implementation"""

from pathlib import Path
from typing import Any

from ..base import BaseHandler, FileHandlerConfig
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class MediaError(FileError):
    """Media specific error"""


class MediaHandler(BaseHandler):
    """Handler for media file operations"""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler."""
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions(
                    [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"]
                ),
                max_file_size=500 * 1024 * 1024,  # 500MB
                metadata={"mime_type": "video/mp4"},
            )
        )

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for media file"""
        extension = path.suffix.lower()
        mime_types = {
            ".mp4": "video/mp4",
            ".avi": "video/x-msvideo",
            ".mov": "video/quicktime",
            ".wmv": "video/x-ms-wmv",
            ".flv": "video/x-flv",
            ".mkv": "video/x-matroska",
        }
        return mime_types.get(extension, "application/octet-stream")

    async def read(self, path: Path) -> FileContent:
        """Read media file content.

        Args:
            path: Path to media file

        Returns:
            Media file content

        Raises:
            MediaError: If file cannot be read
        """
        try:
            if not path.exists():
                raise MediaError(f"File does not exist: {path}")

            content = path.read_bytes()
            metadata = FileMetadata(
                name=path.name,
                mime_type=self._get_mime_type(path),
                size=len(content),
                format=path.suffix.lstrip("."),
            )

            return FileContent(path=path, content=content, metadata=metadata)
        except Exception as e:
            raise MediaError(f"Failed to read media file: {e}") from e

    async def write(self, content: FileContent, path: Path | None = None) -> None:
        """Write media file content.

        Args:
            content: Media content to write
            path: Optional path to write to

        Raises:
            MediaError: If file cannot be written
        """
        try:
            target = path or content.path
            if not isinstance(content.content, bytes):
                raise MediaError("Invalid media content - must be bytes")

            target.write_bytes(content.content)
        except Exception as e:
            raise MediaError(f"Failed to write media file: {e}") from e

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass

    def _get_metadata(self, media: Any) -> dict[str, Any]:
        """Extract metadata from media file."""
        return {
            "duration": media.duration,
            "bitrate": media.bitrate,
            "codec": media.codec,
            "channels": media.channels,
        }
