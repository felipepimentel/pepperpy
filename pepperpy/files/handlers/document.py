"""Document file handler implementation"""

from io import BytesIO
from pathlib import Path
from typing import Any, Iterator, cast

from pypdf import PdfReader
from pypdf._page import PageObject

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from ..utils import ensure_path
from .base import FileHandler


class DocumentHandler(FileHandler[bytes]):
    """Handler for document files"""

    async def read(self, path: PathLike) -> FileContent:
        """Read document file"""
        try:
            file_path = ensure_path(path)
            content = await self._read_content(file_path)

            # Criar PDF reader para extrair informações
            reader = PdfReader(BytesIO(content))

            metadata = self._create_metadata(
                path=file_path,
                file_type=FileType.DOCUMENT,
                mime_type="application/pdf",
                format_str="pdf",
                metadata={
                    "pages": len(reader.pages),
                    "info": reader.metadata or {},
                },
            )

            return FileContent(content=content, metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to read document file: {e!s}", cause=e)

    async def write(
        self,
        content: bytes,
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write document file"""
        try:
            file_path = ensure_path(path)
            await self._write_bytes(content, file_path)
            return file_path
        except Exception as e:
            raise FileError(f"Failed to write document file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> bytes:
        """Read document content"""
        return path.read_bytes()

    async def _write_bytes(self, content: bytes, path: Path) -> None:
        """Write binary content"""
        path.write_bytes(content)

    def get_pages(self, content: bytes) -> Iterator[PageObject]:
        """Get PDF pages"""
        reader = PdfReader(BytesIO(content))
        for page in reader.pages:
            yield cast(PageObject, page)

    def get_images(self, content: bytes) -> Iterator[tuple[str, bytes]]:
        """Extract images from PDF"""
        reader = PdfReader(BytesIO(content))
        for page in reader.pages:
            for image in page.images:
                yield image.name, image.data

    def get_text(self, content: bytes) -> str:
        """Extract text from PDF"""
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() for page in reader.pages)
