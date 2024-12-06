"""CSV file handler implementation."""

import csv
from pathlib import Path
from typing import Any

from ..base import BaseHandler, FileHandlerConfig
from ..exceptions import FileError
from ..types import FileMetadata


class CSVHandler(BaseHandler):
    """Handler for CSV files."""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler."""
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions([".csv"]),
                max_file_size=10 * 1024 * 1024,  # 10MB
                metadata={"mime_type": "text/csv"},
            )
        )

    async def _extract_metadata(self, content: str, path: Path) -> FileMetadata:
        """Extract metadata from CSV content.

        Args:
            content: CSV content
            path: File path

        Returns:
            File metadata

        Raises:
            FileError: If metadata cannot be extracted
        """
        try:
            lines = content.splitlines()
            if not lines:
                return FileMetadata(
                    name=path.name,
                    mime_type="text/csv",
                    size=0,
                    format="csv",
                )

            return FileMetadata(
                name=path.name,
                mime_type="text/csv",
                size=len(content),
                format="csv",
            )
        except Exception as e:
            raise FileError(f"Failed to extract CSV metadata: {e}") from e

    def _process_content(self, content: str) -> list[dict[str, Any]]:
        """Process CSV content."""
        rows = []
        for row in csv.reader(content.splitlines()):
            rows.append({str(i): value for i, value in enumerate(row)})
        return rows
