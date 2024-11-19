"""JSON file handler implementation"""

from pathlib import Path
from typing import Any

import orjson

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import FileHandler


class JSONHandler(FileHandler[dict[str, Any]]):
    """Handler for JSON files"""

    async def read(self, path: PathLike) -> FileContent[dict[str, Any]]:
        """Read JSON file"""
        try:
            file_path = self._to_path(path)
            content = await self._read_content(file_path)
            data = orjson.loads(content)

            metadata = self._create_metadata(
                path=file_path,
                file_type=FileType.JSON,
                mime_type="application/json",
                format_str="json",
            )

            return FileContent(content=data, metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to read JSON file: {e!s}", cause=e)

    async def write(
        self,
        content: dict[str, Any],
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write JSON file"""
        try:
            file_path = self._to_path(path)
            json_str = orjson.dumps(
                content,
                option=orjson.OPT_INDENT_2 | orjson.OPT_SERIALIZE_NUMPY,
            ).decode()
            await self._write_text(json_str, file_path)
            return file_path
        except Exception as e:
            raise FileError(f"Failed to write JSON file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> str:
        """Read JSON content"""
        return path.read_text()

    async def _write_text(self, content: str, path: Path) -> None:
        """Write text content"""
        path.write_text(content)
