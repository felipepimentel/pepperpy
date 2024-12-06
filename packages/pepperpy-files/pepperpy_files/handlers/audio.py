"""Audio file handler implementation."""

from pathlib import Path

from ..base import BaseHandler, FileHandlerConfig
from ..enums import FileType
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class AudioError(FileError):
    """Audio specific error."""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class AudioHandler(BaseHandler):
    """Handler for audio files."""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler.

        Args:
            config: Optional handler configuration
        """
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions(
                    [".mp3", ".wav", ".ogg", ".flac"]
                ),
                max_file_size=100 * 1024 * 1024,  # 100MB
                metadata={"type": FileType.AUDIO, "mime_type": "audio/mpeg"},
            )
        )

    async def _validate_size(self, path: Path) -> None:
        """Validate file size.

        Args:
            path: File path to validate

        Raises:
            AudioError: If file size exceeds limit
        """
        size = path.stat().st_size
        if size > self.config.max_file_size:
            raise AudioError(
                f"File size ({size} bytes) exceeds limit ({self.config.max_file_size} bytes)"
            )

    async def _setup(self) -> None:
        """Setup handler."""
        pass

    async def _teardown(self) -> None:
        """Teardown handler."""
        pass

    async def read(self, path: Path) -> FileContent:
        """Read audio file.

        Args:
            path: Path to audio file

        Returns:
            Audio file content

        Raises:
            AudioError: If file cannot be read
        """
        try:
            await self._validate_size(path)
            with open(path, "rb") as f:
                content = f.read()
            metadata = FileMetadata(
                name=path.name,
                mime_type="audio/mpeg",
                size=len(content),
                format=path.suffix.lstrip("."),
            )
            return FileContent(path=path, content=content, metadata=metadata)
        except Exception as e:
            raise AudioError(f"Failed to read audio file: {e}") from e

    async def write(self, content: FileContent, path: Path | None = None) -> None:
        """Write audio file.

        Args:
            content: Audio content to write
            path: Optional path to write to

        Raises:
            AudioError: If file cannot be written
        """
        try:
            target = path or content.path
            if isinstance(content.content, str):
                content_bytes = content.content.encode(self.config.encoding)
            else:
                content_bytes = (
                    content.content
                    if isinstance(content.content, bytes)
                    else bytes(content.content)
                )

            with open(target, "wb") as f:
                f.write(content_bytes)
        except Exception as e:
            raise AudioError(f"Failed to write audio file: {e}") from e
