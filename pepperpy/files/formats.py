"""Modern file format handlers with enhanced capabilities."""

from pathlib import Path
from typing import Any, Dict, Union

import chardet
import filetype
import openpyxl
import orjson
import pandas as pd
import polars as pl
from bs4 import BeautifulSoup
from pypdf import PdfReader
from python_epub3 import EpubReader  # Biblioteca atualizada para EPUB


class FileHandler:
    """Base class for file handlers with enhanced features."""

    @classmethod
    def detect_encoding(cls, path: Union[str, Path]) -> str:
        """Detect file encoding."""
        with open(path, "rb") as f:
            return chardet.detect(f.read())["encoding"]

    @classmethod
    def detect_mime_type(cls, path: Union[str, Path]) -> str:
        """Detect file MIME type."""
        kind = filetype.guess(path)
        return kind.mime if kind else "application/octet-stream"


class JSONHandler(FileHandler):
    """JSON handler using orjson for better performance."""

    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Dict:
        with open(path, "rb") as f:
            return orjson.loads(f.read())

    @classmethod
    def write(cls, data: Dict, path: Union[str, Path], **kwargs) -> None:
        with open(path, "wb") as f:
            f.write(
                orjson.dumps(
                    data,
                    option=orjson.OPT_INDENT_2 | orjson.OPT_SERIALIZE_NUMPY,
                    default=str,
                )
            )


class PDFHandler(FileHandler):
    """Modern PDF handler with enhanced features."""

    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Dict:
        path_str = str(path)
        reader = PdfReader(path_str)

        # Extract text and metadata
        content = [page.extract_text() for page in reader.pages]
        metadata = reader.metadata

        result = {
            "content": content,
            "metadata": {
                "title": metadata.get("/Title", ""),
                "author": metadata.get("/Author", ""),
                "creator": metadata.get("/Creator", ""),
                "producer": metadata.get("/Producer", ""),
                "pages": len(reader.pages),
            },
        }

        return result


class ExcelHandler(FileHandler):
    """Excel file handler with Pandas/Polars support."""

    @classmethod
    def read(
        cls, path: Union[str, Path], **kwargs
    ) -> Union[Dict[str, Any], pl.DataFrame]:
        engine = kwargs.pop("engine", "polars")

        if engine == "polars":
            return pl.read_excel(path, **kwargs)
        else:
            return pd.read_excel(path, **kwargs)

    @classmethod
    def write(
        cls,
        data: Union[Dict, pl.DataFrame, pd.DataFrame],
        path: Union[str, Path],
        **kwargs,
    ):
        if isinstance(data, pd.DataFrame):
            data.to_excel(path, **kwargs)
        else:
            workbook = openpyxl.Workbook()
            for sheet_name, sheet_data in data.items():
                sheet = workbook.create_sheet(sheet_name)
                for row in sheet_data:
                    sheet.append(row)
            workbook.save(path)


class EbookHandler(FileHandler):
    """Modern ebook handler supporting EPUB format using python-epub3."""

    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Dict:
        book = EpubReader(path)

        content = []
        for item in book.get_items_of_type("application/xhtml+xml"):
            soup = BeautifulSoup(item.get_body_content(), "html.parser")
            content.append(soup.get_text())

        metadata = {
            "title": book.get_metadata("title"),
            "authors": book.get_metadata("creator"),
            "language": book.get_metadata("language"),
            "publisher": book.get_metadata("publisher"),
            "identifier": book.get_metadata("identifier"),
        }

        return {"content": content, "metadata": metadata}


# Register handlers
HANDLERS = {
    ".json": JSONHandler,
    ".pdf": PDFHandler,
    ".xlsx": ExcelHandler,
    ".xls": ExcelHandler,
    ".epub": EbookHandler,
}
