"""Image file handler implementation."""

import io
from pathlib import Path
from typing import Any, Optional

from ..base import BaseHandler, FileHandlerConfig
from ..exceptions import FileError
from ..types import FileContent, FileMetadata

try:
    import PIL

    image_available = True
except ImportError:
    image_available = False

# Definir o módulo como opcional
image_module: Optional[Any] = PIL if image_available else None


class ImageError(FileError):
    """Image specific error."""

    def __init__(self, message: str, original_error: Exception | None = None) -> None:
        super().__init__(message)
        self.original_error = original_error


class ImageHandler(BaseHandler):
    """Handler for image files."""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize image handler.

        Args:
            config: Handler configuration
        """
        if not image_available:
            raise ImageError(
                "Image support requires additional dependencies. "
                "Please install with: pip install Pillow"
            )

        extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions(extensions),
                max_file_size=20 * 1024 * 1024,  # 20MB
                metadata={
                    "type": "image",
                    "mime_type": "image/jpeg",
                },
            )
        )
        self._initialized = False

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file."""
        if not image_available or image_module is None:
            return "image/*"

        try:
            with image_module.Image.open(path) as img:
                format_name = img.format
                if format_name is None:
                    return "image/*"
                return f"image/{format_name.lower()}"
        except Exception as e:
            raise ImageError(f"Failed to get MIME type: {str(e)}", original_error=e)

    def _get_file_type(self, path: Path) -> str:
        """Get file type."""
        return "image"

    def _get_format(self, path: Path) -> str:
        """Get file format."""
        if not image_available or image_module is None:
            return path.suffix.lstrip(".")

        try:
            with image_module.Image.open(path) as img:
                format_name = img.format
                if format_name is None:
                    return path.suffix.lstrip(".")
                return str(format_name.lower())
        except Exception as e:
            raise ImageError(f"Failed to get format: {str(e)}", original_error=e)

    def _to_path(self, file: str | Path) -> Path:
        """Convert to Path object.

        Args:
            file: Path-like object

        Returns:
            Path object
        """
        return Path(file) if isinstance(file, str) else file

    async def read(self, file: str | Path) -> FileContent:
        """Read image file.

        Args:
            file: Path to image file

        Returns:
            Image file content

        Raises:
            ImageError: If reading fails
        """
        try:
            path = self._to_path(file)

            if not image_available or image_module is None:
                raise ImageError("Image support not available")

            with open(path, "rb") as f:
                content = f.read()

            # Get image info
            with image_module.open(io.BytesIO(content)) as img:
                info = {
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "info": dict(img.info),
                }

            file_metadata = FileMetadata(
                name=path.name,
                mime_type=self._get_mime_type(path),
                size=len(content),
                format=self._get_format(path),
                additional_metadata=info,  # Nome correto do parâmetro
            )

            return FileContent(path=path, content=content, metadata=file_metadata)

        except Exception as e:
            raise ImageError(f"Failed to read image file: {str(e)}", original_error=e)

    async def write(self, content: bytes, output: str | Path) -> None:
        """Write image file.

        Args:
            content: Image content
            output: Output path

        Raises:
            ImageError: If writing fails
        """
        try:
            path = self._to_path(output)

            if not image_available or image_module is None:
                raise ImageError("Image support not available")

            # Validate image content
            try:
                image_module.open(io.BytesIO(content))
            except Exception as e:
                raise ImageError("Invalid image content", original_error=e)

            with open(path, "wb") as f:
                f.write(content)

        except Exception as e:
            raise ImageError(f"Failed to write image file: {str(e)}", original_error=e)

    async def cleanup(self) -> None:
        """Cleanup resources."""
        pass

    def _get_metadata(self, image: Any, path: Path) -> dict[str, Any]:
        """Extract metadata from image."""
        info = {
            k: str(v) if not isinstance(v, (int, float, bool, str)) else v
            for k, v in image.info.items()
        }

        return {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
            "info": info,
        }

    def _validate_content(self, content: Any) -> None:
        """Validate image content."""
        if not isinstance(content, bytes | bytearray | memoryview):  # Usando union type
            raise ValueError("Content must be bytes, bytearray or memoryview")
