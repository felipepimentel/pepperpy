"""Spreadsheet file handler implementation"""

import io
from io import StringIO
from pathlib import Path
from typing import Any

try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    pd = None
    HAS_PANDAS = False

from ..base import BaseHandler, FileHandlerConfig
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class SpreadsheetError(FileError):
    """Spreadsheet specific error"""


class SpreadsheetHandler(BaseHandler):
    """Handler for spreadsheet file operations"""

    def __init__(self, config: FileHandlerConfig | None = None) -> None:
        """Initialize handler.

        Args:
            config: Optional handler configuration
        """
        super().__init__(
            config
            or FileHandlerConfig(
                allowed_extensions=self._convert_extensions(
                    [".xls", ".xlsx", ".ods", ".csv"]
                ),
                max_file_size=50 * 1024 * 1024,  # 50MB
                metadata={"mime_type": "application/vnd.ms-excel"},
            )
        )
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize handler"""
        if not HAS_PANDAS:
            raise SpreadsheetError(
                "Pandas support not available - please install pandas"
            )
        if not pd:
            raise SpreadsheetError("Pandas module not available")
        self._initialized = True

    async def read(self, path: Path) -> FileContent:
        """Read spreadsheet file content.

        Args:
            path: Path to spreadsheet file

        Returns:
            Spreadsheet content

        Raises:
            SpreadsheetError: If file cannot be read
        """
        try:
            if not path.exists():
                raise SpreadsheetError(f"File does not exist: {path}")

            if not self._initialized:
                raise RuntimeError("Handler not initialized")

            if not pd:
                raise SpreadsheetError("Pandas module not available")

            # Read spreadsheet using pandas
            df = pd.read_excel(path) if path.suffix != ".csv" else pd.read_csv(path)
            content = df.to_csv(index=False).encode(self.config.encoding)

            metadata = FileMetadata(
                name=path.name,
                mime_type=self._get_mime_type(path),
                size=len(content),
                format=path.suffix.lstrip("."),
            )

            return FileContent(path=path, content=content, metadata=metadata)

        except Exception as e:
            raise SpreadsheetError(f"Failed to read spreadsheet: {e}") from e

    async def write(self, content: FileContent, path: Path | None = None) -> None:
        """Write spreadsheet content.

        Args:
            content: Spreadsheet content
            path: Optional path to write to

        Raises:
            SpreadsheetError: If file cannot be written
        """
        try:
            target = path or content.path
            if not self._initialized:
                raise RuntimeError("Handler not initialized")

            if not pd:
                raise SpreadsheetError("Pandas module not available")

            if not isinstance(content.content, (str, bytes)):
                raise SpreadsheetError("Invalid content type - must be string or bytes")

            # Convert content to string if needed
            data = (
                content.content.decode(self.config.encoding)
                if isinstance(content.content, bytes)
                else content.content
            )

            # Parse CSV data into DataFrame using StringIO
            df = pd.read_csv(StringIO(data))

            # Write based on extension
            if target.suffix == ".csv":
                df.to_csv(target, index=False)
            else:
                df.to_excel(target, index=False)

        except Exception as e:
            raise SpreadsheetError(f"Failed to write spreadsheet: {e}") from e

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for spreadsheet file"""
        extension = path.suffix.lower()
        mime_types = {
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xls": "application/vnd.ms-excel",
            ".csv": "text/csv",
            ".ods": "application/vnd.oasis.opendocument.spreadsheet",
        }
        return mime_types.get(extension, "application/octet-stream")

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self._initialized = False

    def _validate_content(self, content: Any) -> None:
        """Validate spreadsheet content."""
        if not isinstance(content, str | bytes | io.IOBase):
            raise ValueError("Content must be string, bytes or file-like object")

    def _process_sheet(self, sheet: Any) -> list[dict[str, Any]]:
        """Process spreadsheet sheet."""
        if not pd:
            raise SpreadsheetError("Pandas module not available")

        if not isinstance(sheet, pd.DataFrame | pd.Series):
            raise ValueError("Sheet must be a pandas DataFrame or Series")

        rows = []
        for row in sheet.values:
            row_dict = {str(col): value for col, value in enumerate(row)}
            rows.append(row_dict)
        return rows
