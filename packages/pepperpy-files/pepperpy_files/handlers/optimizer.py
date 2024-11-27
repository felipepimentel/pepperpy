"""File optimizer handler implementation"""

from pathlib import Path
from typing import Any, Dict, cast

from bko.files.exceptions import FileError
from bko.files.handlers.base import BaseFileHandler
from bko.files.types import FileContent, FileMetadata
from PIL import Image


class FileOptimizerHandler(BaseFileHandler):
    """Handler for file optimization operations"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize handler"""
        super().__init__(*args, **kwargs)
        self._supported_image_formats = {".jpg", ".jpeg", ".png", ".webp"}
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize handler"""
        await super().initialize()
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup handler"""
        await super().cleanup()
        self._initialized = False

    async def read(self, path: Path, **kwargs: Dict[str, Any]) -> FileContent:
        """Read and optimize file content"""
        path = self._to_path(path)

        if not path.exists():
            raise FileError(f"File does not exist: {path}")

        if not self._initialized:
            raise RuntimeError("Handler not initialized")

        if path.suffix.lower() not in self._supported_image_formats:
            raise FileError(f"Unsupported file format: {path.suffix}")

        try:
            # Read and optimize image
            with Image.open(path) as img:
                # Convert to RGB if needed
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # Create optimized image in memory
                optimized = self._optimize_image(img, **kwargs)

                # Get optimized size
                optimized_size = len(optimized)

                return FileContent(
                    content=optimized,
                    metadata=FileMetadata(
                        name=path.name,
                        mime_type=self._get_mime_type(path),
                        path=path,
                        type="image",
                        extension=path.suffix,
                        format="binary",
                        size=optimized_size,
                    ),
                )
        except Exception as e:
            raise FileError(f"Failed to optimize file: {e}", cause=e)

    async def write(self, path: Path, content: FileContent, **kwargs: Dict[str, Any]) -> None:
        """Write optimized file content"""
        path = self._to_path(path)

        if not self._initialized:
            raise RuntimeError("Handler not initialized")

        if not isinstance(content.content, bytes):
            raise FileError("Invalid content type")

        if path.suffix.lower() not in self._supported_image_formats:
            raise FileError(f"Unsupported output format: {path.suffix}")

        try:
            with open(path, "wb") as f:
                f.write(content.content)
        except Exception as e:
            raise FileError(f"Failed to write optimized file: {e}", cause=e)

    def _optimize_image(self, image: Image.Image, **kwargs: Dict[str, Any]) -> bytes:
        """Optimize image"""
        quality = cast(int, kwargs.get("quality", 85))
        format_str = cast(str, kwargs.get("format", "JPEG"))

        # Create a new bytes buffer
        from io import BytesIO

        buffer = BytesIO()

        # Save optimized image to buffer
        image.save(
            buffer,
            format=format_str,
            quality=quality,
            optimize=True,
        )

        # Get the buffer content
        return buffer.getvalue()

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        extension = path.suffix.lower()
        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        return mime_types.get(extension, "application/octet-stream")
