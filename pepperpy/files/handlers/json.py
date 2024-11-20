"""JSON file handler implementation"""

import json

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class JSONHandler(BaseFileHandler, FileHandler[dict]):
    """Handler for JSON files"""

    async def read(self, file: PathLike) -> FileContent[dict]:
        """Read JSON file"""
        try:
            path = self._to_path(file)
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.DATA,
                mime_type="application/json",
                format_str="json",
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read JSON file: {e}", cause=e)

    async def write(self, content: dict, output: PathLike) -> None:
        """Write JSON file"""
        try:
            path = self._to_path(output)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, indent=2)
        except Exception as e:
            raise FileError(f"Failed to write JSON file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
