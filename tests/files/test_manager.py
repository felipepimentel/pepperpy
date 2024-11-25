"""Tests for file manager"""

from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from pepperpy.files.config import FileManagerConfig
from pepperpy.files.exceptions import FileError
from pepperpy.files.manager import FileManager
from pepperpy.files.types import FileContent, FileMetadata


@pytest.fixture
def mock_file_path():
    """Fixture for mock file path"""
    return Path("/test/data.txt")


@pytest.fixture
def manager_config():
    """Fixture for file manager config"""
    return FileManagerConfig(
        base_path=Path("/test"),
        allowed_extensions=set([".txt", ".md", ".json", ".yaml", ".pdf"]),
        max_file_size=1024 * 1024,  # 1MB
        metadata={"environment": "test"},
    )


@pytest.fixture
def file_manager(manager_config):
    """Fixture for file manager"""
    return FileManager(config=manager_config)


@pytest.mark.asyncio
async def test_file_manager_initialization(file_manager):
    """Test file manager initialization"""
    assert not file_manager.is_initialized
    await file_manager.initialize()
    assert file_manager.is_initialized


@pytest.mark.asyncio
async def test_file_manager_cleanup(file_manager):
    """Test file manager cleanup"""
    await file_manager.initialize()
    await file_manager.cleanup()
    assert not file_manager.is_initialized


@pytest.mark.asyncio
async def test_file_manager_get_handler(file_manager):
    """Test getting file handler"""
    await file_manager.initialize()

    # Test getting handlers for different file types
    txt_handler = file_manager.get_handler(Path("test.txt"))
    assert txt_handler is not None

    json_handler = file_manager.get_handler(Path("test.json"))
    assert json_handler is not None

    yaml_handler = file_manager.get_handler(Path("test.yaml"))
    assert yaml_handler is not None

    pdf_handler = file_manager.get_handler(Path("test.pdf"))
    assert pdf_handler is not None


@pytest.mark.asyncio
async def test_file_manager_invalid_extension(file_manager):
    """Test file manager with invalid extension"""
    await file_manager.initialize()

    with pytest.raises(FileError, match="No handler found for extension"):
        file_manager.get_handler(Path("test.invalid"))


@pytest.mark.asyncio
async def test_file_manager_not_initialized(file_manager, mock_file_path):
    """Test file manager when not initialized"""
    with pytest.raises(RuntimeError, match="not initialized"):
        await file_manager.read(mock_file_path)


@pytest.mark.asyncio
async def test_file_manager_read(file_manager, mock_file_path):
    """Test file manager read operation"""
    await file_manager.initialize()

    content = FileContent(
        content="test content",
        metadata=FileMetadata(
            name=mock_file_path.name,
            mime_type="text/plain",
            path=mock_file_path,
            type="text/plain",
            extension=".txt",
            format="utf-8",
            size=1024,
        ),
    )

    handler = file_manager.get_handler(mock_file_path)
    handler.read = AsyncMock(return_value=content)

    result = await file_manager.read(mock_file_path)
    assert result == content


@pytest.mark.asyncio
async def test_file_manager_write(file_manager, mock_file_path):
    """Test file manager write operation"""
    await file_manager.initialize()

    content = FileContent(
        content="test content",
        metadata=FileMetadata(
            name=mock_file_path.name,
            mime_type="text/plain",
            path=mock_file_path,
            type="text/plain",
            extension=".txt",
            format="utf-8",
            size=1024,
        ),
    )

    handler = file_manager.get_handler(mock_file_path)
    handler.write = AsyncMock()

    await file_manager.write(mock_file_path, content)
    handler.write.assert_called_once_with(mock_file_path, content)
