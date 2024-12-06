"""Compression file handler implementation"""

import gzip
import zipfile
from pathlib import Path

from ..base import BaseHandler, FileHandlerConfig
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class CompressionError(FileError):
    """Compression specific error"""


class CompressionHandler(BaseHandler):
    """Handler for compressed files"""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler."""
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions([".gz", ".zip"]),
                max_file_size=100 * 1024 * 1024,  # 100MB
                metadata={"mime_type": "application/gzip"},
            )
        )

    def _to_path(self, file: Path | str) -> Path:
        """Convert PathLike to Path"""
        return Path(file) if isinstance(file, str) else file

    def _ensure_bytes(self, content: str | bytes) -> bytes:
        """Ensure content is bytes.

        Args:
            content: Content to convert

        Returns:
            Content as bytes
        """
        if isinstance(content, str):
            return content.encode(self.config.encoding)
        return content

    async def read(self, file: Path | str) -> FileContent:
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
                raise CompressionError(f"Unsupported compression format: {path.suffix}")

            metadata = FileMetadata(
                name=path.name,
                mime_type=f"application/{path.suffix[1:]}",
                size=len(content),
                format=path.suffix[1:],
            )

            return FileContent(path=path, content=content, metadata=metadata)
        except Exception as e:
            raise CompressionError(f"Failed to read compressed file: {e}") from e

    async def write(self, content: FileContent, path: Path | None = None) -> None:
        """Write compressed file"""
        try:
            target = path or content.path
            data = self._ensure_bytes(content.content)

            if target.suffix == ".gz":
                with gzip.open(target, "wb") as f:
                    f.write(data)
            elif target.suffix == ".zip":
                with zipfile.ZipFile(target, "w") as z:
                    z.writestr("content", data)
            else:
                raise CompressionError(
                    f"Unsupported compression format: {target.suffix}"
                )
        except Exception as e:
            raise CompressionError(f"Failed to write compressed file: {e}") from e

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
