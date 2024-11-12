"""PDF file handler implementation"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import PyPDF2

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class PDFHandler(BaseHandler):
    """Handler for PDF files"""

    async def read(self, path: Path) -> FileContent:
        """Read PDF file"""
        try:
            metadata = await self._get_metadata(path)

            # Read PDF content
            with open(path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                content = {
                    "pages": len(reader.pages),
                    "text": [page.extract_text() for page in reader.pages],
                    "metadata": reader.metadata,
                }

            return FileContent(content=content, metadata=metadata, format="pdf")
        except Exception as e:
            raise FileError(f"Failed to read PDF file: {str(e)}", cause=e)

    async def write(
        self, path: Path, content: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> FileMetadata:
        """Write PDF file"""
        try:
            writer = PyPDF2.PdfWriter()

            # Add pages
            if isinstance(content.get("pages"), list):
                for page in content["pages"]:
                    writer.add_page(page)

            # Add metadata
            if metadata:
                writer.add_metadata(metadata)

            # Write to file
            with open(path, "wb") as file:
                writer.write(file)

            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write PDF file: {str(e)}", cause=e)

    async def merge(self, paths: List[Path], output: Path) -> FileMetadata:
        """Merge multiple PDF files"""
        try:
            merger = PyPDF2.PdfMerger()

            for path in paths:
                merger.append(str(path))

            with open(output, "wb") as file:
                merger.write(file)

            return await self._get_metadata(output)
        except Exception as e:
            raise FileError(f"Failed to merge PDF files: {str(e)}", cause=e)
