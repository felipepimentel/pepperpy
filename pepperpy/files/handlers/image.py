"""Image file handler implementation"""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from PIL import Image, ImageEnhance, ImageFilter

from ..base import FileHandler
from ..exceptions import FileError
from ..types import ImageInfo


class ImageHandler(FileHandler):
    """Handler for image files"""

    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

    async def read(self, path: Path, mode: Optional[str] = None) -> Image.Image:
        """Read image file"""
        try:
            image = Image.open(path)
            if mode and image.mode != mode:
                image = image.convert(mode)
            return image
        except Exception as e:
            raise FileError(f"Failed to read image: {str(e)}", cause=e)

    async def write(self, path: Path, image: Image.Image, **kwargs: Any) -> None:
        """Write image file"""
        try:
            image.save(path, **kwargs)
        except Exception as e:
            raise FileError(f"Failed to write image: {str(e)}", cause=e)

    async def get_info(self, path: Path) -> ImageInfo:
        """Get image information"""
        try:
            with Image.open(path) as img:
                return ImageInfo(
                    width=img.width,
                    height=img.height,
                    mode=img.mode,
                    format=img.format or path.suffix[1:].upper(),
                    dpi=img.info.get("dpi"),
                    exif=img.getexif() if hasattr(img, "getexif") else None,
                )
        except Exception as e:
            raise FileError(f"Failed to get image info: {str(e)}", cause=e)

    async def resize(
        self,
        image: Image.Image,
        size: Tuple[int, int],
        resample: int = Image.Resampling.LANCZOS,
        keep_aspect: bool = True,
    ) -> Image.Image:
        """Resize image"""
        try:
            if keep_aspect:
                image.thumbnail(size, resample)
                return image
            return image.resize(size, resample)
        except Exception as e:
            raise FileError(f"Failed to resize image: {str(e)}", cause=e)

    async def apply_filters(self, image: Image.Image, filters: Dict[str, Any]) -> Image.Image:
        """Apply multiple filters"""
        try:
            result = image.copy()

            for filter_name, params in filters.items():
                if filter_name == "blur":
                    result = result.filter(ImageFilter.GaussianBlur(params.get("radius", 2)))
                elif filter_name == "sharpen":
                    result = result.filter(ImageFilter.SHARPEN)
                elif filter_name == "brightness":
                    enhancer = ImageEnhance.Brightness(result)
                    result = enhancer.enhance(params.get("factor", 1.0))
                elif filter_name == "contrast":
                    enhancer = ImageEnhance.Contrast(result)
                    result = enhancer.enhance(params.get("factor", 1.0))
                elif filter_name == "color":
                    enhancer = ImageEnhance.Color(result)
                    result = enhancer.enhance(params.get("factor", 1.0))
                else:
                    raise FileError(f"Unknown filter: {filter_name}")

            return result

        except Exception as e:
            raise FileError(f"Failed to apply filters: {str(e)}", cause=e)

    async def create_thumbnail(
        self, path: Path, output_path: Path, size: Tuple[int, int], quality: int = 85
    ) -> None:
        """Create image thumbnail"""
        try:
            image = await self.read(path)
            thumb = await self.resize(image, size)
            await self.write(output_path, thumb, quality=quality, optimize=True)
        except Exception as e:
            raise FileError(f"Failed to create thumbnail: {str(e)}", cause=e)

    async def validate(self, path: Path) -> bool:
        """Validate image file"""
        try:
            if path.suffix.lower() not in self.SUPPORTED_FORMATS:
                return False

            with Image.open(path) as img:
                img.verify()
            return True

        except Exception:
            return False
