"""Tests for JSON file handler"""

from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pepperpy.files.exceptions import FileError
from pepperpy.files.handlers.json import JSONFileHandler
from pepperpy.files.types import FileContent, FileMetadata


def create_mock_file(content: str) -> Mock:
    """Create a mock file-like object with JSON content"""
    mock = Mock()
    handle = StringIO(content)
    mock.__enter__ = Mock(return_value=handle)
    mock.__exit__ = Mock(return_value=None)
    mock.read = Mock(return_value=content)
    mock.write = Mock()
    return mock


@pytest.fixture
def json_handler():
    """Fixture for JSON handler"""
    return JSONFileHandler()


@pytest.mark.asyncio
async def test_json_handler_read(json_handler):
    """Test JSON handler read operation"""
    await json_handler.initialize()

    test_content = '{"test": "data", "number": 42}'
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.json"
    mock_path.suffix = ".json"

    with patch("builtins.open", return_value=create_mock_file(test_content)):
        content = await json_handler.read(mock_path)
        assert isinstance(content.content, dict)
        assert content.content == {"test": "data", "number": 42}
        assert content.metadata.mime_type == "application/json"
        assert content.metadata.extension == ".json"


@pytest.mark.asyncio
async def test_json_handler_write(json_handler):
    """Test JSON handler write operation"""
    await json_handler.initialize()

    test_file = Path("/test/test.json")
    json_data = {"test": "data", "number": 42}
    content = FileContent(
        content=json_data,
        metadata=FileMetadata(
            name="test.json",
            mime_type="application/json",
            path=test_file,
            type="application/json",
            extension=".json",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = False
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.json"
    mock_path.suffix = ".json"

    mock_file = create_mock_file("")
    with patch("pathlib.Path", return_value=mock_path), patch(
        "builtins.open", return_value=mock_file
    ):
        await json_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_json_handler_invalid_json(json_handler):
    """Test JSON handler with invalid JSON file"""
    await json_handler.initialize()

    test_content = "invalid json content"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "invalid.json"
    mock_path.suffix = ".json"

    with patch("builtins.open", return_value=create_mock_file(test_content)), pytest.raises(
        FileError, match="Invalid JSON"
    ):
        await json_handler.read(mock_path)


@pytest.mark.asyncio
async def test_json_handler_invalid_content(json_handler):
    """Test JSON handler with non-serializable content"""
    await json_handler.initialize()

    test_file = Path("/test/test.json")
    content = FileContent(
        content={"key": object()},  # Non-serializable nested object
        metadata=FileMetadata(
            name="test.json",
            mime_type="application/json",
            path=test_file,
            type="application/json",
            extension=".json",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = False
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.json"
    mock_path.suffix = ".json"

    mock_file = create_mock_file("")
    with patch("pathlib.Path", return_value=mock_path), patch(
        "builtins.open", return_value=mock_file
    ), pytest.raises(FileError, match="Failed to write file"):
        await json_handler.write(test_file, content)
