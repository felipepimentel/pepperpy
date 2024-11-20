"""Spreadsheet file handler implementation"""

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class SpreadsheetHandler(BaseFileHandler, FileHandler[bytes]):
    """Handler for spreadsheet files"""

    async def read(self, file: PathLike) -> FileContent[bytes]:
        """Read spreadsheet file"""
        try:
            path = self._to_path(file)
            with open(path, "rb") as f:
                content = f.read()

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.DATA,
                mime_type=("application/vnd.openxmlformats-officedocument" ".spreadsheetml.sheet"),
                format_str=path.suffix[1:],
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read spreadsheet file: {e}", cause=e)

    async def write(self, content: bytes, output: PathLike) -> None:
        """Write spreadsheet file"""
        try:
            path = self._to_path(output)
            with open(path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise FileError(f"Failed to write spreadsheet file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
