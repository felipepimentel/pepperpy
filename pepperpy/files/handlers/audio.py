"""Audio file handler implementation"""

from ..exceptions import FileError
from ..types import FileContent, FileType, MediaInfo, PathLike
from .base import BaseFileHandler, FileHandler


class AudioHandler(BaseFileHandler, FileHandler[bytes]):
    """Handler for audio files"""

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read audio file"""
        try:
            path = self._to_path(file)
            with open(path, "rb") as f:
                content = f.read()

            # Create media info
            media_info = MediaInfo(
                duration=0.0,  # Implementar extração real
                bitrate=0,
                codec="",
                format=path.suffix[1:],
            )

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.AUDIO,
                mime_type=f"audio/{path.suffix[1:]}",
                format_str=path.suffix[1:],
                extra={"media_info": media_info.to_dict()},
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read audio file: {e}", cause=e)

    async def write(self, content: bytes, output: PathLike) -> None:
        """Write audio file"""
        try:
            path = self._to_path(output)
            with open(path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise FileError(f"Failed to write audio file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
