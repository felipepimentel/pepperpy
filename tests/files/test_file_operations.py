"""Tests for file operations"""

from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest

from pepperpy.files.exceptions import FileError
from pepperpy.files.handlers.base import BaseFileHandler
from pepperpy.files.operations import FileOperations
from pepperpy.files.types import FileContent, FileMetadata


@pytest.fixture
def mock_handler():
    """Fixture for mock handler"""
    handler = Mock(spec=BaseFileHandler)
    handler.read = AsyncMock()
    handler.write = AsyncMock()
    return handler


@pytest.fixture
def mock_path():
    """Fixture for mock path"""
    path = Mock(spec=Path)
    path.exists.return_value = True
    path.name = "test.txt"
    path.suffix = ".txt"
    path.__str__ = Mock(return_value="/test/test.txt")
    return path


@pytest.fixture
def file_operations(mock_handler):
    """Fixture for file operations"""
    ops = FileOperations()
    ops.register_handler(".txt", mock_handler)
    return ops


@pytest.mark.asyncio
async def test_file_operations_initialize(file_operations):
    """Test file operations initialization"""
    await file_operations.initialize()
    assert file_operations._initialized


@pytest.mark.asyncio
async def test_file_operations_cleanup(file_operations):
    """Test file operations cleanup"""
    await file_operations.initialize()
    await file_operations.cleanup()
    assert not file_operations._initialized
    assert not file_operations._handlers


@pytest.mark.asyncio
async def test_file_operations_read(file_operations, mock_handler, mock_path):
    """Test file read operation"""
    await file_operations.initialize()

    expected_content = FileContent(
        content="test",
        metadata=FileMetadata(
            name="test.txt",
            mime_type="text/plain",
            path=mock_path,
            type="text",
            extension=".txt",
            format="utf-8",
            size=4,
        ),
    )
    mock_handler.read.return_value = expected_content

    result = await file_operations.read(mock_path)
    assert result == expected_content
    mock_handler.read.assert_called_once_with(mock_path)


@pytest.mark.asyncio
async def test_file_operations_write(file_operations, mock_handler, mock_path):
    """Test file write operation"""
    await file_operations.initialize()

    content = FileContent(
        content="test",
        metadata=FileMetadata(
            name="test.txt",
            mime_type="text/plain",
            path=mock_path,
            type="text",
            extension=".txt",
            format="utf-8",
            size=4,
        ),
    )

    await file_operations.write(mock_path, content)
    mock_handler.write.assert_called_once_with(mock_path, content)


@pytest.mark.asyncio
async def test_file_operations_unknown_extension(file_operations):
    """Test error handling for unknown extension"""
    await file_operations.initialize()

    unknown_path = Mock(spec=Path)
    unknown_path.exists.return_value = True
    unknown_path.suffix = ".unknown"
    unknown_path.__str__ = Mock(return_value="/test/file.unknown")

    with pytest.raises(FileError, match="No handler registered"):
        await file_operations.read(unknown_path)


@pytest.mark.asyncio
async def test_file_operations_not_initialized(file_operations, mock_path):
    """Test error when operations not initialized"""
    with pytest.raises(RuntimeError, match="not initialized"):
        await file_operations.read(mock_path)
