"""Media file handler implementation"""

from datetime import datetime
from pathlib import Path
from typing import Any

from ..exceptions import FileError
from ..types import FileContent, FileMetadata, FileType, MediaInfo, PathLike, ensure_path
from .base import FileHandler


class MediaHandler(FileHandler[bytes]):
    """Handler for media files"""

    async def read(self, path: PathLike) -> FileContent:
        """Read media file"""
        try:
            file_path = ensure_path(path)
            content = await self._read_content(file_path)

            # Extrair informações de mídia
            media_info = await self._extract_media_info(file_path)

            metadata = FileMetadata(
                name=file_path.name,
                size=file_path.stat().st_size,
                file_type=FileType.MEDIA,
                mime_type=self._get_mime_type(file_path),
                format=file_path.suffix.lstrip(".").lower(),
                created_at=datetime.fromtimestamp(file_path.stat().st_ctime),
                modified_at=datetime.fromtimestamp(file_path.stat().st_mtime),
                path=file_path,
                media_info=media_info,
            )

            return FileContent(content=content, metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to read media file: {e!s}", cause=e)

    async def write(
        self,
        content: bytes,
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write media file"""
        try:
            file_path = ensure_path(path)
            await self._write_bytes(content, file_path)
            return file_path
        except Exception as e:
            raise FileError(f"Failed to write media file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> bytes:
        """Read media content"""
        return path.read_bytes()

    async def _write_bytes(self, content: bytes, path: Path) -> None:
        """Write binary content"""
        path.write_bytes(content)

    async def _extract_media_info(self, path: Path) -> MediaInfo:
        """Extract media information from file"""
        try:
            # Implementar extração real de metadados de mídia
            # Por exemplo, usando ffmpeg-python ou similar
            return MediaInfo(
                duration=0.0,
                bitrate=0,
                codec="unknown",
            )
        except Exception as e:
            raise FileError(f"Failed to extract media info: {e!s}", cause=e)

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for media file"""
        extension = path.suffix.lower()
        mime_types = {
            ".mp4": "video/mp4",
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".avi": "video/x-msvideo",
            ".mov": "video/quicktime",
        }
        return mime_types.get(extension, "application/octet-stream")
