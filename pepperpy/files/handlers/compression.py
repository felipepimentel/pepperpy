"""Compression file handler implementation"""

import gzip
import zipfile

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class CompressionHandler(BaseFileHandler, FileHandler[bytes]):
    """Handler for compressed files"""

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
                file_type=FileType.ARCHIVE,
                mime_type=f"application/{path.suffix[1:]}",
                format_str=path.suffix[1:],
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
