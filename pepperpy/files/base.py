"""Base file handling functionality"""

import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator, Optional

import magic

from .exceptions import FileError
from .types import FileMetadata, FileStats


class FileHandler(ABC):
    """Base class for file handlers"""

    def __init__(self) -> None:
        self._buffer_size = 8192
        self._magic = magic.Magic(mime=True)

    async def get_metadata(self, path: Path) -> FileMetadata:
        """Get file metadata"""
        try:
            stat = path.stat()
            mime_type = self._magic.from_file(str(path))

            # Calculate hash
            sha256 = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(self._buffer_size), b""):
                    sha256.update(chunk)

            return FileMetadata(
                path=path,
                name=path.name,
                extension=path.suffix.lower(),
                size=stat.st_size,
                created_at=datetime.fromtimestamp(stat.st_ctime),
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                mime_type=mime_type,
                hash=sha256.hexdigest(),
                encoding=self._detect_encoding(path),
            )
        except Exception as e:
            raise FileError(f"Failed to get metadata: {str(e)}", cause=e)

    async def get_stats(self, path: Path) -> FileStats:
        """Get file statistics"""
        try:
            metadata = await self.get_metadata(path)

            return FileStats(
                metadata=metadata,
                blocks=metadata.size // self._buffer_size + 1,
                is_empty=metadata.size == 0,
                is_binary=self._is_binary(path),
                permissions=oct(path.stat().st_mode)[-3:],
                is_compressed=self._is_compressed(path),
            )
        except Exception as e:
            raise FileError(f"Failed to get stats: {str(e)}", cause=e)

    async def read_chunks(
        self, path: Path, chunk_size: Optional[int] = None
    ) -> AsyncIterator[bytes]:
        """Read file in chunks"""
        try:
            chunk_size = chunk_size or self._buffer_size
            with open(path, "rb") as f:
                while chunk := f.read(chunk_size):
                    yield chunk
        except Exception as e:
            raise FileError(f"Failed to read chunks: {str(e)}", cause=e)

    async def write_chunks(self, path: Path, chunks: AsyncIterator[bytes]) -> None:
        """Write chunks to file"""
        try:
            with open(path, "wb") as f:
                async for chunk in chunks:
                    f.write(chunk)
        except Exception as e:
            raise FileError(f"Failed to write chunks: {str(e)}", cause=e)

    async def copy_with_progress(
        self, src: Path, dst: Path, callback: Optional[callable] = None
    ) -> None:
        """Copy file with progress tracking"""
        try:
            total_size = src.stat().st_size
            copied = 0

            async for chunk in self.read_chunks(src):
                await self.write_chunks(dst, [chunk])
                copied += len(chunk)
                if callback:
                    await callback(copied, total_size)

        except Exception as e:
            raise FileError(f"Failed to copy file: {str(e)}", cause=e)

    def _detect_encoding(self, path: Path) -> Optional[str]:
        """Detect file encoding"""
        try:
            import chardet

            with open(path, "rb") as f:
                raw = f.read(self._buffer_size)
                result = chardet.detect(raw)
                return result["encoding"] if result["confidence"] > 0.7 else None
        except ImportError:
            return None

    def _is_binary(self, path: Path, sample_size: int = 8192) -> bool:
        """Check if file is binary"""
        try:
            with open(path, "rb") as f:
                sample = f.read(sample_size)
                return b"\x00" in sample
        except Exception:
            return False

    def _is_compressed(self, path: Path) -> bool:
        """Check if file is compressed"""
        compressed_types = {
            "application/gzip",
            "application/x-bzip2",
            "application/x-xz",
            "application/zip",
            "application/x-rar-compressed",
        }
        return self._magic.from_file(str(path)) in compressed_types

    @abstractmethod
    async def read(self, path: Path) -> Any:
        """Read file content"""
        pass

    @abstractmethod
    async def write(self, path: Path, content: Any, **kwargs: Any) -> None:
        """Write content to file"""
        pass

    @abstractmethod
    async def validate(self, path: Path) -> bool:
        """Validate file format"""
        pass
