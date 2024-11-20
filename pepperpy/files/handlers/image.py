"""Image file handler implementation"""

from PIL import Image as PILImage

from ..exceptions import FileError
from ..types import FileContent, FileType, ImageInfo, PathLike
from .base import BaseFileHandler, FileHandler


class ImageHandler(BaseFileHandler, FileHandler[bytes]):
    """Handler for image files"""

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read image file"""
        try:
            path = self._to_path(file)
            with open(path, "rb") as f:
                content = f.read()

            # Extract image info
            with PILImage.open(path) as img:
                image_info = ImageInfo(
                    width=img.width,
                    height=img.height,
                    channels=len(img.getbands()),
                    mode=img.mode,
                    format=img.format or path.suffix[1:],
                )

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.IMAGE,
                mime_type=f"image/{path.suffix[1:]}",
                format_str=path.suffix[1:],
                extra={"image_info": image_info.to_dict()},
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
