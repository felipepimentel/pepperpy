"""CSV file handler implementation"""

import csv
from pathlib import Path
from typing import Any, Dict, cast

from bko.files.exceptions import FileError
from bko.files.handlers.text import TextFileHandler
from bko.files.types import FileContent, FileMetadata


class CSVFileHandler(TextFileHandler):
    """Handler for CSV file operations"""

    async def read(self, path: Path, **kwargs: Dict[str, Any]) -> FileContent:
        """Read CSV file content"""
        if not path.exists():
            raise FileError("File does not exist")

        encoding = cast(str, kwargs.get("encoding", "utf-8"))
        delimiter = cast(str, kwargs.get("delimiter", ","))

        try:
            with open(path, "r", encoding=encoding, newline="") as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                try:
                    rows = list(reader)
                    if not rows:
                        raise FileError("Empty CSV file")

                    if not reader.fieldnames:
                        raise FileError("Invalid CSV format: no headers found")

                    expected_fields = len(reader.fieldnames)
                    if not all(len(row) == expected_fields for row in rows):
                        raise FileError("Invalid CSV format: inconsistent number of fields")

                    return FileContent(
                        content=rows,
                        metadata=FileMetadata(
                            name=path.name,
                            mime_type="text/csv",
                            path=path,
                            type="text/csv",
                            extension=path.suffix,
                            format=encoding,
                            size=path.stat().st_size,
                        ),
                    )
                except csv.Error:
                    raise FileError("Invalid CSV format")
        except Exception as e:
            raise FileError(f"Failed to read CSV file: {e}", cause=e)

    async def write(self, path: Path, content: FileContent, **kwargs: Dict[str, Any]) -> None:
        """Write CSV file content"""
        if not isinstance(content.content, list):
            raise FileError("Invalid CSV content")

        if not content.content:
            raise FileError("Invalid CSV content: cannot be empty")

        # Verificar se o diretório pai existe
        if not path.parent.exists():
            raise FileError("Parent directory does not exist")

        encoding = cast(str, kwargs.get("encoding", "utf-8"))
        delimiter = cast(str, kwargs.get("delimiter", ","))

        try:
            with open(path, "w", encoding=encoding, newline="") as f:
                if not content.content:
                    return

                fieldnames = list(content.content[0].keys())
                writer = csv.DictWriter(
                    f, fieldnames=fieldnames, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL
                )
                writer.writeheader()
                writer.writerows(content.content)
        except Exception as e:
            raise FileError(f"Failed to write CSV file: {e}", cause=e)
