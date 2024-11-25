"""Tests for Markdown file handler"""

import pytest

from pepperpy.files.config import FileHandlerConfig
from pepperpy.files.handlers.markdown import MarkdownFileHandler
from pepperpy.files.types import FileContent, FileMetadata


@pytest.fixture
def markdown_handler(handler_config, test_files):
    """Fixture for Markdown handler"""
    config = FileHandlerConfig(
        base_path=test_files,
        allowed_extensions={".md"},
        max_file_size=1024 * 1024,
        metadata={"environment": "test"},
    )
    return MarkdownFileHandler(config)


@pytest.mark.asyncio
async def test_markdown_handler_read(markdown_handler, test_files):
    """Test Markdown handler read operation"""
    await markdown_handler.initialize()

    test_file = test_files / "test.md"
    content = await markdown_handler.read(test_file)

    assert isinstance(content, FileContent)
    assert content.content == "# Test\nContent with *markdown*"
    assert content.metadata.mime_type == "text/markdown"
    assert content.metadata.extension == ".md"


@pytest.mark.asyncio
async def test_markdown_handler_write(markdown_handler, test_write_dir):
    """Test Markdown handler write operation"""
    await markdown_handler.initialize()

    test_file = test_write_dir / "test.md"
    md_content = "# Test\nContent with *markdown*"
    content = FileContent(
        content=md_content,
        metadata=FileMetadata(
            name=test_file.name,
            mime_type="text/markdown",
            path=test_file,
            type="text/markdown",
            extension=".md",
            format="utf-8",
            size=100,
        ),
    )

    await markdown_handler.write(test_file, content)
    assert test_file.exists()
    assert test_file.read_text(encoding="utf-8") == md_content
