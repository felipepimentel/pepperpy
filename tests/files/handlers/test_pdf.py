"""Tests for PDF file handler"""

from io import BytesIO
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pepperpy.files.exceptions import FileError
from pepperpy.files.handlers.pdf import PDFFileHandler
from pepperpy.files.types import FileContent, FileMetadata


def create_mock_file(content: bytes = b"") -> Mock:
    """Create a mock file-like object with PDF content"""
    mock = Mock()
    handle = BytesIO(content)
    mock.__enter__ = Mock(return_value=handle)
    mock.__exit__ = Mock(return_value=None)
    mock.read = Mock(return_value=content)
    mock.write = Mock()
    return mock


@pytest.fixture
def pdf_handler():
    """Fixture for PDF handler"""
    return PDFFileHandler()


@pytest.mark.asyncio
async def test_pdf_handler_read(pdf_handler):
    """Test PDF handler read operation"""
    await pdf_handler.initialize()

    test_content = b"%PDF-1.4\ntest pdf content"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.pdf"
    mock_path.suffix = ".pdf"

    mock_file = create_mock_file(test_content)
    with patch("builtins.open", return_value=mock_file):
        content = await pdf_handler.read(mock_path)
        assert isinstance(content.content, bytes)
        assert content.content == test_content
        assert content.metadata.mime_type == "application/pdf"
        assert content.metadata.extension == ".pdf"


@pytest.mark.asyncio
async def test_pdf_handler_write(pdf_handler):
    """Test PDF handler write operation"""
    await pdf_handler.initialize()

    test_file = Path("/test/test.pdf")
    pdf_content = b"%PDF-1.4\ntest pdf content"
    content = FileContent(
        content=pdf_content,
        metadata=FileMetadata(
            name="test.pdf",
            mime_type="application/pdf",
            path=test_file,
            type="application/pdf",
            extension=".pdf",
            format="binary",
            size=len(pdf_content),
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = False
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.pdf"
    mock_path.suffix = ".pdf"

    mock_file = create_mock_file()
    with patch("pathlib.Path", return_value=mock_path), patch(
        "builtins.open", return_value=mock_file
    ):
        await pdf_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_pdf_handler_invalid_content(pdf_handler):
    """Test PDF handler with invalid content"""
    await pdf_handler.initialize()

    test_file = Path("/test/test.pdf")
    content = FileContent(
        content=b"invalid pdf content",  # Missing PDF header
        metadata=FileMetadata(
            name="test.pdf",
            mime_type="application/pdf",
            path=test_file,
            type="application/pdf",
            extension=".pdf",
            format="binary",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = False
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.pdf"
    mock_path.suffix = ".pdf"

    mock_file = create_mock_file()
    with patch("pathlib.Path", return_value=mock_path), patch(
        "builtins.open", return_value=mock_file
    ), pytest.raises(FileError, match="Invalid PDF content"):
        await pdf_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_pdf_handler_invalid_pdf(pdf_handler):
    """Test PDF handler with invalid PDF file"""
    await pdf_handler.initialize()

    test_content = b"invalid pdf content"  # Missing PDF header
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "invalid.pdf"
    mock_path.suffix = ".pdf"

    mock_file = create_mock_file(test_content)
    with patch("builtins.open", return_value=mock_file), pytest.raises(
        FileError, match="Invalid PDF content"
    ):
        await pdf_handler.read(mock_path)
