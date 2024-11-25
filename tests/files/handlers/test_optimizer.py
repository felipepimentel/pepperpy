"""Tests for file optimizer handler"""

from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pepperpy.files.config import FileHandlerConfig
from pepperpy.files.exceptions import FileError
from pepperpy.files.handlers.optimizer import FileOptimizerHandler
from pepperpy.files.types import FileContent, FileMetadata


def create_mock_file(content: str) -> Mock:
    """Create a mock file-like object"""
    mock = Mock()
    handle = StringIO(content)
    mock.__enter__ = Mock(return_value=handle)
    mock.__exit__ = Mock(return_value=None)
    mock.read = Mock(return_value=content)
    mock.write = Mock()
    return mock


@pytest.fixture
def optimizer_handler():
    """Fixture for optimizer handler"""
    config = FileHandlerConfig(
        base_path=Path("/test"),
        allowed_extensions={".txt", ".json", ".yaml", ".md"},
        max_file_size=1024 * 1024,
        metadata={"environment": "test"},
    )
    handler = FileOptimizerHandler(config)
    handler._supported_image_formats = {".txt", ".json", ".yaml", ".md"}
    return handler


@pytest.mark.asyncio
async def test_optimizer_text_optimization(optimizer_handler):
    """Test text content optimization"""
    await optimizer_handler.initialize()

    test_content = "  Test content  \n\n"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.txt"
    mock_path.suffix = ".txt"

    mock_file = create_mock_file(test_content)
    with patch("builtins.open", return_value=mock_file):
        content = await optimizer_handler.read(mock_path)
        assert isinstance(content, FileContent)
        assert isinstance(content.content, str)
        assert content.content.strip() == "Test content"


@pytest.mark.asyncio
async def test_optimizer_write_operation(optimizer_handler):
    """Test optimizer write operation"""
    await optimizer_handler.initialize()

    test_content = "  Test content  \n\n"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.txt"
    mock_path.suffix = ".txt"
    mock_path.stat.return_value = Mock(st_size=len(test_content))

    content = FileContent(
        content=test_content,
        metadata=FileMetadata(
            name=mock_path.name,
            mime_type="text/plain",
            path=mock_path,
            type="text/plain",
            extension=".txt",
            format="utf-8",
            size=len(test_content),
        ),
    )

    mock_file = create_mock_file("")
    with patch("pathlib.Path", return_value=mock_path), patch(
        "builtins.open", return_value=mock_file
    ):
        await optimizer_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_optimizer_dict_optimization(optimizer_handler):
    """Test dictionary content optimization"""
    await optimizer_handler.initialize()

    test_data = {"key1": "value1", "key2": None, "key3": "value3"}
    content = FileContent(
        content=test_data,
        metadata=FileMetadata(
            name="test.json",
            mime_type="application/json",
            path=Path("/test/test.json"),
            type="application/json",
            extension=".json",
            format="utf-8",
            size=100,
        ),
    )

    # Test high compression
    optimizer_handler.compression_level = "high"
    optimized = await optimizer_handler.optimize(content)
    assert isinstance(optimized.content, dict)
    assert "key2" not in optimized.content
    assert len(optimized.content) == 2

    # Test medium compression
    optimizer_handler.compression_level = "medium"
    optimized = await optimizer_handler.optimize(content)
    assert len(optimized.content) == 2

    # Test low compression
    optimizer_handler.compression_level = "low"
    optimized = await optimizer_handler.optimize(content)
    assert len(optimized.content) == 3


@pytest.mark.asyncio
async def test_optimizer_unsupported_type(optimizer_handler):
    """Test optimizer with unsupported file type"""
    await optimizer_handler.initialize()

    mock_path = Mock(spec=Path)
    mock_path.suffix = ".unsupported"

    content = FileContent(
        content="test",
        metadata=FileMetadata(
            name="test.unsupported",
            mime_type="application/octet-stream",
            path=mock_path,
            type="binary",
            extension=".unsupported",
            format="binary",
            size=4,
        ),
    )

    with pytest.raises(FileError, match="Unsupported file type"):
        await optimizer_handler.optimize(content)


@pytest.mark.asyncio
async def test_optimizer_invalid_compression_level(optimizer_handler):
    """Test optimizer with invalid compression level"""
    await optimizer_handler.initialize()

    with pytest.raises(ValueError, match="Invalid compression level"):
        optimizer_handler.compression_level = "invalid"
