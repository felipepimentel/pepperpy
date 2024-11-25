"""Tests for YAML file handler"""

from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest
import yaml

from pepperpy.files.exceptions import FileError
from pepperpy.files.handlers.yaml import YAMLFileHandler
from pepperpy.files.types import FileContent, FileMetadata


@pytest.fixture
def yaml_handler():
    """Fixture for YAML handler"""
    return YAMLFileHandler()


@pytest.mark.asyncio
async def test_yaml_handler_read(yaml_handler):
    """Test YAML handler read operation"""
    await yaml_handler.initialize()

    test_content = "test: data\nlist: [1, 2, 3]"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.yaml"
    mock_path.suffix = ".yaml"

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m):
        content = await yaml_handler.read(mock_path)
        assert isinstance(content.content, dict)
        assert content.content == {"test": "data", "list": [1, 2, 3]}
        assert content.metadata.mime_type == "application/yaml"
        assert content.metadata.extension == ".yaml"


@pytest.mark.asyncio
async def test_yaml_handler_write(yaml_handler):
    """Test YAML handler write operation"""
    await yaml_handler.initialize()

    test_file = Path("/test/test.yaml")
    yaml_data = {"test": "data", "list": [1, 2, 3]}
    content = FileContent(
        content=yaml_data,
        metadata=FileMetadata(
            name="test.yaml",
            mime_type="application/yaml",
            path=test_file,
            type="application/yaml",
            extension=".yaml",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.yaml"
    mock_path.suffix = ".yaml"

    m = mock_open()
    with patch("builtins.open", m):
        await yaml_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_yaml_handler_invalid_yaml(yaml_handler):
    """Test YAML handler with invalid YAML file"""
    await yaml_handler.initialize()

    test_content = "invalid: yaml: content: ["
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "invalid.yaml"
    mock_path.suffix = ".yaml"

    # Mock that raises YAMLError when reading
    def mock_load(*args, **kwargs):
        raise yaml.YAMLError("Invalid YAML")

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m), patch("yaml.safe_load", side_effect=mock_load), pytest.raises(
        FileError, match="Invalid YAML format"
    ):
        await yaml_handler.read(mock_path)


@pytest.mark.asyncio
async def test_yaml_handler_invalid_content(yaml_handler):
    """Test YAML handler with non-serializable content"""
    await yaml_handler.initialize()

    class NonSerializable:
        pass

    test_file = Path("/test/test.yaml")
    content = FileContent(
        content={"key": NonSerializable()},  # Non-serializable nested object
        metadata=FileMetadata(
            name="test.yaml",
            mime_type="application/yaml",
            path=test_file,
            type="application/yaml",
            extension=".yaml",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.yaml"
    mock_path.suffix = ".yaml"

    # Mock that raises YAMLError when dumping
    def mock_dump(*args, **kwargs):
        raise yaml.YAMLError("Cannot serialize object")

    with patch("pathlib.Path", return_value=mock_path), patch("builtins.open", mock_open()), patch(
        "yaml.safe_dump", side_effect=mock_dump
    ), pytest.raises(FileError, match="Failed to write file: Invalid YAML format"):
        await yaml_handler.write(test_file, content)


@pytest.mark.asyncio
async def test_yaml_handler_empty_content(yaml_handler):
    """Test YAML handler with empty content"""
    await yaml_handler.initialize()

    test_content = ""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "empty.yaml"
    mock_path.suffix = ".yaml"

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m):
        content = await yaml_handler.read(mock_path)
        assert isinstance(content.content, dict)
        assert content.content == {}  # Empty YAML should return empty dict


@pytest.mark.asyncio
async def test_yaml_handler_invalid_extension(yaml_handler):
    """Test YAML handler with invalid file extension"""
    await yaml_handler.initialize()

    test_file = Path("/test/test.invalid")
    content = FileContent(
        content={"test": "data"},
        metadata=FileMetadata(
            name="test.invalid",
            mime_type="application/yaml",
            path=test_file,
            type="application/yaml",
            extension=".invalid",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.invalid"
    mock_path.suffix = ".invalid"

    with patch("pathlib.Path", return_value=mock_path), pytest.raises(
        FileError, match="Invalid file extension"
    ):
        await yaml_handler.write(test_file, content)
