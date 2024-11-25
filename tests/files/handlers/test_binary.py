"""Tests for binary file handler"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pepperpy.files.config import FileHandlerConfig
from pepperpy.files.handlers.binary import BinaryFileHandler
from pepperpy.files.types import FileContent, FileMetadata


@pytest.fixture
def mock_file_path():
    """Fixture for mock file path"""
    return Path("/test/data.bin")


@pytest.fixture
def handler_config():
    """Fixture for handler config"""
    return FileHandlerConfig(
        base_path=Path("/test"),
        allowed_extensions={".bin", ".dat"},
        max_file_size=1024 * 1024,
        metadata={"environment": "test"},
    )


@pytest.fixture
def binary_handler(handler_config):
    """Fixture for binary handler"""
    return BinaryFileHandler(handler_config)


@pytest.mark.asyncio
async def test_binary_handler_read(binary_handler, mock_file_path):
    """Test binary handler read operation"""
    await binary_handler.initialize()

    binary_content = b"Hello, world!"
    mock_stat = Mock()
    mock_stat.st_size = 1024

    with patch("builtins.open", mock_open(read_data=binary_content)), patch(
        "pathlib.Path.stat", return_value=mock_stat
    ):
        content = await binary_handler.read(mock_file_path)
        assert content.content == binary_content
        assert content.metadata.mime_type == "application/octet-stream"


@pytest.mark.asyncio
async def test_binary_handler_write(binary_handler, test_write_dir):
    """Test binary handler write operation"""
    await binary_handler.initialize()

    test_file = test_write_dir / "test.bin"
    content = FileContent(
        content=b"test binary content",
        metadata=FileMetadata(
            name=test_file.name,
            mime_type="application/octet-stream",
            path=test_file,
            type="application/octet-stream",
            extension=".bin",
            format="binary",
            size=100,
        ),
    )

    await binary_handler.write(test_file, content)
    assert test_file.exists()
    assert test_file.read_bytes() == b"test binary content"


def mock_open(read_data=b""):
    """Create mock open function"""
    mock = Mock()
    mock.return_value.__enter__ = Mock(return_value=Mock(read=Mock(return_value=read_data)))
    mock.return_value.__exit__ = Mock()
    mock.return_value.write = Mock()
    return mock
