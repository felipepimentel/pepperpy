"""Image file handler implementation"""

from pathlib import Path

from PIL import Image as PILImage

from ..exceptions import FileError
from ..types import FileContent, FileMetadata, FileType, ImageInfo, PathLike
from .base import BaseFileHandler


class ImageHandler(BaseFileHandler[bytes]):
    """Handler for image files"""

    def _to_path(self, file: PathLike) -> Path:
        """Convert PathLike to Path"""
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return f"image/{path.suffix[1:]}"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.IMAGE

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix[1:]

    def _get_extra_metadata(self, path: Path) -> dict:
        """Get extra metadata for image"""
        with PILImage.open(path) as img:
            image_info = ImageInfo(
                width=img.width,
                height=img.height,
                channels=len(img.getbands()),
                mode=img.mode,
                format=img.format or path.suffix[1:],
            )
            return {"image_info": image_info.to_dict()}

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read image file"""
        try:
            path = self._to_path(file)
            with open(path, "rb") as f:
                content = f.read()

            base_metadata = self._create_metadata(path=path, size=len(content))
            extra_metadata = self._get_extra_metadata(path)

            # Criar um novo FileMetadata com os dados extras
            metadata = FileMetadata(
                path=base_metadata.path,
                size=base_metadata.size,
                type=base_metadata.type,
                mime_type=base_metadata.mime_type,
                format=base_metadata.format,
                **extra_metadata,
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read image file: {e}", cause=e)

    async def write(self, content: bytes, output: PathLike) -> None:
        """Write image file"""
        try:
            path = self._to_path(output)
            with open(path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise FileError(f"Failed to write image file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
