"""Image file handler implementation"""

from io import BytesIO
from pathlib import Path
from typing import Any

from PIL import Image, ImageFile

from ..exceptions import FileError
from ..types import FileContent, FileType, ImageInfo, PathLike
from .base import FileHandler


class ImageHandler(FileHandler[Image.Image]):
    """Handler for image files"""

    async def read(self, path: PathLike) -> FileContent[Image.Image]:
        """Read image file"""
        try:
            file_path = self._to_path(path)
            content = await self._read_content(file_path)
            image = Image.open(BytesIO(content))

            # Extrair informações da imagem
            info = ImageInfo(
                width=image.width,
                height=image.height,
                format=image.format or "",
                mode=image.mode,
                channels=len(image.getbands()),
                bits=getattr(image, "bits", 8),
                dpi=image.info.get("dpi"),
            )

            metadata = self._create_metadata(
                path=file_path,
                file_type=FileType.IMAGE,
                mime_type=f"image/{image.format.lower()}" if image.format else "image/unknown",
                format_str=image.format.lower() if image.format else "unknown",
                metadata={
                    "image_info": info,
                    "original_info": dict(image.info),
                },
            )

            return FileContent(content=image, metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to read image file: {e!s}", cause=e)

    async def write(
        self,
        content: Image.Image,
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write image file"""
        try:
            file_path = self._to_path(path)

            # Configurar opções de salvamento
            save_kwargs = {}
            if metadata:
                save_kwargs.update(metadata)

            # Salvar imagem
            content.save(file_path, **save_kwargs)
            return file_path

        except Exception as e:
            raise FileError(f"Failed to write image file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> bytes:
        """Read image content"""
        return path.read_bytes()

    async def _write_text(self, content: str, path: Path) -> None:
        """Write text content"""
        path.write_text(content)

    async def _write_bytes(self, content: bytes, path: Path) -> None:
        """Write binary content"""
        path.write_bytes(content)

    def optimize(
        self,
        image: Image.Image,
        quality: int = 85,
        max_size: tuple[int, int] | None = None,
    ) -> Image.Image:
        """
        Optimize image

        Args:
            image: Image to optimize
            quality: JPEG quality (1-100)
            max_size: Maximum (width, height)

        Returns:
            Image.Image: Optimized image
        """
        try:
            # Criar cópia para não modificar original
            img = image.copy()

            # Redimensionar se necessário
            if max_size:
                img.thumbnail(max_size)

            # Otimizar
            ImageFile.MAXBLOCK = img.size[0] * img.size[1]
            opt_buffer = BytesIO()
            img.save(opt_buffer, format=img.format, quality=quality, optimize=True)
            opt_buffer.seek(0)
            return Image.open(opt_buffer)

        except Exception as e:
            raise FileError(f"Failed to optimize image: {e!s}", cause=e)
