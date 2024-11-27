"""Document file handler implementation"""

from pathlib import Path

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler


class DocumentHandler(BaseFileHandler[bytes]):
    """Handler for document files"""

    def _to_path(self, file: PathLike) -> Path:
        """Convert PathLike to Path"""
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.DOCUMENT

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix[1:]

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read document file"""
        try:
            path = self._to_path(file)
            with open(path, "rb") as f:
                content = f.read()

            metadata = self._create_metadata(path=path, size=len(content))

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read document file: {e}", cause=e)

    async def write(self, content: bytes, output: PathLike) -> None:
        """Write document file"""
        try:
            path = self._to_path(output)
            with open(path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise FileError(f"Failed to write document file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
