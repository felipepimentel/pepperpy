"""PDF file handler implementation"""

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class PDFHandler(BaseFileHandler, FileHandler[bytes]):
    """Handler for PDF files"""

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read PDF file"""
        try:
            path = self._to_path(file)
            with open(path, "rb") as f:
                content = f.read()

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.DOCUMENT,
                mime_type="application/pdf",
                format_str="pdf",
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read PDF file: {e}", cause=e)

    async def write(self, content: bytes, output: PathLike) -> None:
        """Write PDF file"""
        try:
            path = self._to_path(output)
            with open(path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise FileError(f"Failed to write PDF file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
