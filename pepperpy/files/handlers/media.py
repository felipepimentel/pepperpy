"""Media file handler implementation"""

from pathlib import Path
from typing import Any, Dict

from pepperpy.files.exceptions import FileError
from pepperpy.files.handlers.base import BaseFileHandler
from pepperpy.files.types import FileContent, FileMetadata


class MediaHandler(BaseFileHandler):
    """Handler for media file operations"""

    async def read(self, path: Path, **kwargs: Dict[str, Any]) -> FileContent:
        """Read media file content"""
        path = self._to_path(path)
        
        if not path.exists():
            raise FileError(f"File does not exist: {path}")

        try:
            with open(path, "rb") as f:
                content = f.read()

            return FileContent(
                content=content,
                metadata=FileMetadata(
                    name=path.name,
                    mime_type=self._get_mime_type(path),
                    path=path,
                    type="media",
                    extension=path.suffix,
                    format="binary",
                    size=path.stat().st_size
                )
            )
        except Exception as e:
            raise FileError(f"Failed to read media file: {e}", cause=e)

    async def write(self, path: Path, content: FileContent, **kwargs: Dict[str, Any]) -> None:
        """Write media file content"""
        path = self._to_path(path)

        if not isinstance(content.content, bytes):
            raise FileError("Invalid media content")

        try:
            with open(path, "wb") as f:
                f.write(content.content)
        except Exception as e:
            raise FileError(f"Failed to write media file: {e}", cause=e)

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
