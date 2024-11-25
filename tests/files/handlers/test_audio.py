"""Tests for audio file handler"""

from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest

from pepperpy.files.exceptions import FileError
from pepperpy.files.handlers.audio import AudioFileHandler
from pepperpy.files.types import FileContent, FileMetadata


@pytest.fixture
def audio_handler():
    """Fixture for audio handler"""
    return AudioFileHandler()


@pytest.mark.asyncio
async def test_audio_handler_read(audio_handler):
    """Test audio handler read operation"""
    await audio_handler.initialize()

    test_content = b"test audio content"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.mp3"
    mock_path.suffix = ".mp3"
    mock_path.__str__ = Mock(return_value="/test/test.mp3")

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m):
        content = await audio_handler.read(mock_path)
        assert isinstance(content.content, bytes)
        assert content.content == test_content


@pytest.mark.asyncio
async def test_audio_handler_write(audio_handler):
    """Test audio handler write operation"""
    await audio_handler.initialize()

    test_content = b"test audio content"
    content = FileContent(
        content=test_content,
        metadata=FileMetadata(
            name="test.mp3",
            mime_type="audio/mpeg",
            path=Path("/test/test.mp3"),
            type="audio",
            extension=".mp3",
            format="binary",
            size=len(test_content),
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.mp3"
    mock_path.suffix = ".mp3"
    mock_path.__str__ = Mock(return_value="/test/test.mp3")

    m = mock_open()
    with patch("builtins.open", m):
        await audio_handler.write(mock_path, content)
        m.assert_called_once_with(mock_path, "wb")
        handle = m()
        handle.write.assert_called_once_with(test_content)


@pytest.mark.asyncio
async def test_audio_handler_invalid_content(audio_handler):
    """Test audio handler with invalid content"""
    await audio_handler.initialize()

    test_file = Path("/test/test.mp3")
    content = FileContent(
        content="invalid content type",  # Should be bytes
        metadata=FileMetadata(
            name="test.mp3",
            mime_type="audio/mpeg",
            path=test_file,
            type="audio",
            extension=".mp3",
            format="binary",
            size=0,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.mp3"
    mock_path.suffix = ".mp3"
    mock_path.__str__ = Mock(return_value="/test/test.mp3")

    with pytest.raises(FileError, match="Invalid audio content"):
        await audio_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_audio_handler_unsupported_format(audio_handler):
    """Test audio handler with unsupported format"""
    await audio_handler.initialize()

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.name = "test.ogg"
    mock_path.suffix = ".ogg"
    mock_path.__str__ = Mock(return_value="/test/test.ogg")

    with pytest.raises(FileError, match="Invalid file extension: .ogg"):
        await audio_handler.read(mock_path)


@pytest.mark.asyncio
async def test_audio_handler_empty_content(audio_handler):
    """Test audio handler with empty content"""
    await audio_handler.initialize()

    content = FileContent(
        content=b"",  # Empty content
        metadata=FileMetadata(
            name="test.mp3",
            mime_type="audio/mpeg",
            path=Path("/test/test.mp3"),
            type="audio",
            extension=".mp3",
            format="binary",
            size=0,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.mp3"
    mock_path.suffix = ".mp3"
    mock_path.__str__ = Mock(return_value="/test/test.mp3")

    with pytest.raises(FileError, match="Invalid audio content: content cannot be empty"):
        await audio_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_audio_handler_size_validation(audio_handler):
    """Test audio handler size validation"""
    await audio_handler.initialize()

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=audio_handler.config.max_file_size + 1)
    mock_path.name = "large.mp3"
    mock_path.suffix = ".mp3"
    mock_path.__str__ = Mock(return_value="/test/large.mp3")

    with pytest.raises(FileError, match="File too large"):
        await audio_handler.read(mock_path)
