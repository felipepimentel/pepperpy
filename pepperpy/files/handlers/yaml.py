"""YAML file handler implementation"""

from datetime import datetime
from pathlib import Path
from typing import Any, cast

import yaml

from ..exceptions import FileError
from ..types import FileContent, FileMetadata, FileType, PathLike, ensure_path
from .base import FileHandler


class YAMLHandler(FileHandler[dict[str, Any]]):
    """Handler for YAML files"""

    async def read(self, path: PathLike) -> FileContent:
        """Read YAML file"""
        try:
            file_path = ensure_path(path)
            content = yaml.safe_load(file_path.read_text())

            metadata = FileMetadata(
                name=file_path.name,
                size=file_path.stat().st_size,
                file_type=FileType.CONFIG,
                mime_type="application/x-yaml",
                format="yaml",
                created_at=datetime.fromtimestamp(file_path.stat().st_ctime),
                modified_at=datetime.fromtimestamp(file_path.stat().st_mtime),
                path=file_path,
            )

            return FileContent(content=cast(dict[str, Any], content), metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to read YAML file: {e!s}", cause=e)

    async def write(
        self,
        content: dict[str, Any],
        path: PathLike,
        **kwargs: Any,
    ) -> Path:
        """Write YAML file"""
        try:
            file_path = ensure_path(path)
            yaml.dump(content, file_path.open("w"), **kwargs)
            return file_path
        except Exception as e:
            raise FileError(f"Failed to write YAML file: {e!s}", cause=e)

    async def _read_content(self, path: Path) -> str:
        """Read YAML content"""
        return path.read_text()

    async def _write_text(self, content: str, path: Path) -> None:
        """Write YAML content"""
        path.write_text(content)

    async def _write_bytes(self, content: bytes, path: Path) -> None:
        """Write binary content"""
        path.write_bytes(content)
