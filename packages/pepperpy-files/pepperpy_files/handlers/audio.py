"""Audio file handler implementation"""

from pathlib import Path

from ...core.exceptions import PepperPyError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandlerConfig


class AudioFileHandler(BaseFileHandler[bytes]):
    """Audio file handler implementation"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__(
            config=FileHandlerConfig(
                base_path=Path("."),
                allowed_extensions={".mp3", ".wav", ".ogg", ".m4a"},
                max_file_size=500 * 1024 * 1024,  # 500MB
                metadata={
                    "type": FileType.AUDIO,
                    "mime_type": "audio/mpeg",  # Default to MP3
                },
            )
        )

    def _ensure_initialized(self) -> None:
        """Ensure handler is initialized"""
        if not self._initialized:
            raise RuntimeError("Handler is not initialized")

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read audio file"""
        self._ensure_initialized()
        try:
            path = Path(file) if isinstance(file, str) else file
            self._validate_path(path)
            self._validate_size(path)

            content = path.read_bytes()
            metadata = self._create_metadata(path=path, size=len(content))
            return FileContent(content=content, metadata=metadata)

        except Exception as e:
            raise PepperPyError(f"Failed to read audio file: {e}", cause=e)

    async def write(self, content: bytes, output: PathLike) -> None:
        """Write audio file"""
        self._ensure_initialized()
        try:
            path = Path(output) if isinstance(output, str) else output
            self._validate_path(path.parent)

            if len(content) > self.config.max_file_size:
                raise PepperPyError(
                    f"Content size ({len(content)} bytes) exceeds limit "
                    f"({self.config.max_file_size} bytes)"
                )

            path.write_bytes(content)

        except Exception as e:
            raise PepperPyError(f"Failed to write audio file: {e}", cause=e)

    def _validate_path(self, path: Path) -> None:
        """Validate file path"""
        if not path.exists():
            raise PepperPyError(f"File not found: {path}")
        if not path.is_file():
            raise PepperPyError(f"Not a file: {path}")
        if path.suffix not in self.config.allowed_extensions:
            raise PepperPyError(f"Invalid file extension: {path.suffix}")

    def _validate_size(self, path: Path) -> None:
        """Validate file size"""
        size = path.stat().st_size
        if size > self.config.max_file_size:
            raise PepperPyError(
                f"File size ({size} bytes) exceeds limit ({self.config.max_file_size} bytes)"
            )

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "audio/mpeg"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.AUDIO

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix.lstrip(".")
