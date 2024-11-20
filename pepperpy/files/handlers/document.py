"""Document file handler implementation"""

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class DocumentHandler(BaseFileHandler, FileHandler[bytes]):
    """Handler for document files"""

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read document file"""
        try:
            path = self._to_path(file)
            with open(path, "rb") as f:
                content = f.read()

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.DOCUMENT,
                mime_type=(
                    "application/vnd.openxmlformats-officedocument" ".wordprocessingml.document"
                ),
                format_str=path.suffix[1:],
            )

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
