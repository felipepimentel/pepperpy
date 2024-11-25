"""Compression file handler implementation"""

import gzip
import zipfile
from pathlib import Path

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler


class CompressionHandler(BaseFileHandler[bytes]):
    """Handler for compressed files"""

    def _to_path(self, file: PathLike) -> Path:
        """Convert PathLike to Path"""
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return f"application/{path.suffix[1:]}"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.ARCHIVE

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix[1:]

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read compressed file"""
        try:
            path = self._to_path(file)
            if path.suffix == ".gz":
                with gzip.open(path, "rb") as f:
                    content = f.read()
            elif path.suffix == ".zip":
                with zipfile.ZipFile(path, "r") as z:
                    content = z.read(z.namelist()[0])
            else:
                raise FileError(f"Unsupported compression format: {path.suffix}")

            metadata = self._create_metadata(
                path=path,
                size=len(content)
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read compressed file: {e}", cause=e)

    async def write(self, content: bytes, output: PathLike) -> None:
        """Write compressed file"""
        try:
            path = self._to_path(output)
            if path.suffix == ".gz":
                with gzip.open(path, "wb") as f:
                    f.write(content)
            elif path.suffix == ".zip":
                with zipfile.ZipFile(path, "w") as z:
                    z.writestr("content", content)
            else:
                raise FileError(f"Unsupported compression format: {path.suffix}")
        except Exception as e:
            raise FileError(f"Failed to write compressed file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
