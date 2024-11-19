"""PDF file handler implementation"""

from io import BytesIO
from pathlib import Path
from typing import Any, cast

from pypdf import PdfReader

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike, ensure_path
from .base import FileHandler


class PDFHandler(FileHandler[bytes]):
    """Handler for PDF files"""

    async def read(self, path: PathLike) -> FileContent:
        """Read PDF file"""
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
            raise FileError(f"Failed to read PDF file: {e!s}", cause=e)

    async def write(
        self,
        content: bytes,
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write PDF file"""
        try:
            file_path = Path(path)
            await self._write_bytes(content, file_path)
            return file_path
        except Exception as e:
            raise FileError(f"Failed to write PDF file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> bytes:
        """Read PDF content"""
        return path.read_bytes()

    async def _write_text(self, content: str, path: Path) -> None:
        """Write text content"""
        path.write_text(content)

    async def _write_bytes(self, content: bytes, path: Path) -> None:
        """Write binary content"""
        path.write_bytes(content)

    async def _parse_pdf(self, content: bytes) -> bytes:
        """Parse PDF content"""
        try:
            # Criar um BytesIO para passar para o PdfReader
            pdf_stream = BytesIO(content)
            reader = PdfReader(pdf_stream)
            return cast(bytes, reader)
        except Exception as e:
            raise FileError(f"Failed to parse PDF: {e!s}", cause=e)
