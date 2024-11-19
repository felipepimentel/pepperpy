"""Spreadsheet file handler implementation"""

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from ..exceptions import FileError
from ..types import FileContent, FileMetadata, FileType, PathLike, ensure_path
from .base import FileHandler


class SpreadsheetHandler(FileHandler[pd.DataFrame]):
    """Handler for spreadsheet files"""

    async def read(self, path: PathLike) -> FileContent:
        """Read spreadsheet file"""
        try:
            file_path = ensure_path(path)

            # Ler arquivo com pandas
            if file_path.suffix == ".xlsx":
                content = pd.read_excel(str(file_path))  # pandas requer str
            else:
                content = pd.read_csv(str(file_path))  # pandas requer str

            metadata = FileMetadata(
                name=file_path.name,
                size=file_path.stat().st_size,
                file_type=FileType.SPREADSHEET,
                mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                format="xlsx" if file_path.suffix == ".xlsx" else "csv",
                created_at=datetime.fromtimestamp(file_path.stat().st_ctime),
                modified_at=datetime.fromtimestamp(file_path.stat().st_mtime),
                path=file_path,
                metadata={
                    "columns": list(content.columns),
                    "rows": len(content),
                },
            )

            return FileContent(content=content, metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to read spreadsheet file: {e!s}", cause=e)

    async def write(
        self,
        content: pd.DataFrame,
        path: PathLike,
        metadata: dict[str, Any] | None = None,
    ) -> Path:
        """Write spreadsheet file"""
        file_path = ensure_path(path)
        if file_path.suffix == ".xlsx":
            content.to_excel(str(file_path), index=False)  # pandas requer str
        else:
            content.to_csv(str(file_path), index=False)  # pandas requer str
        return file_path

    async def _read_content(self, path: Path) -> bytes:
        """Read spreadsheet content"""
        return path.read_bytes()

    async def _write_text(self, content: str, path: Path) -> None:
        """Write text content"""
        path.write_text(content)

    async def _write_bytes(self, content: bytes, path: Path) -> None:
        """Write binary content"""
        path.write_bytes(content)
