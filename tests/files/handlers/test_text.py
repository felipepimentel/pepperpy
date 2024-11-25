"""Tests for text file handler"""

import pytest

from pepperpy.files.handlers.text import TextFileHandler
from pepperpy.files.types import FileContent, FileMetadata


@pytest.fixture
def text_handler():
    """Fixture for text handler"""
    return TextFileHandler()


@pytest.mark.asyncio
async def test_text_handler_read(text_handler, test_files):
    """Test text handler read operation"""
    await text_handler.initialize()

    test_file = test_files / "test.txt"
    content = await text_handler.read(test_file)

    assert isinstance(content, FileContent)
    assert content.content == "Test content"
    assert content.metadata.mime_type == "text/plain"
    assert content.metadata.extension == ".txt"


@pytest.mark.asyncio
async def test_text_handler_read_with_encoding(text_handler, test_write_dir):
    """Test text handler read with specific encoding"""
    await text_handler.initialize()

    test_file = test_write_dir / "test.txt"
    test_content = "Test content with encoding"
    test_file.write_text(test_content, encoding="utf-16")

    content = await text_handler.read(test_file, encoding="utf-16")
    assert content.content == test_content
    assert content.metadata.format == "utf-16"


@pytest.mark.asyncio
async def test_text_handler_write(text_handler, test_write_dir):
    """Test text handler write operation"""
    await text_handler.initialize()

    test_file = test_write_dir / "test.txt"
    text_content = "Test content for writing"
    content = FileContent(
        content=text_content,
        metadata=FileMetadata(
            name=test_file.name,
            mime_type="text/plain",
            path=test_file,
            type="text/plain",
            extension=".txt",
            format="utf-8",
            size=len(text_content.encode("utf-8")),
        ),
    )

    await text_handler.write(test_file, content)
    assert test_file.exists()
    assert test_file.read_text(encoding="utf-8") == text_content


@pytest.mark.asyncio
async def test_text_handler_write_with_encoding(text_handler, test_write_dir):
    """Test text handler write with specific encoding"""
    await text_handler.initialize()

    test_file = test_write_dir / "test.txt"
    text_content = "Test content with encoding"
    content = FileContent(
        content=text_content,
        metadata=FileMetadata(
            name=test_file.name,
            mime_type="text/plain",
            path=test_file,
            type="text/plain",
            extension=".txt",
            format="utf-16",
            size=len(text_content.encode("utf-16")),
        ),
    )

    await text_handler.write(test_file, content, encoding="utf-16")
    assert test_file.exists()
    assert test_file.read_text(encoding="utf-16") == text_content
