"""Tests for base file operations"""

from pathlib import Path

import pytest

from pepperpy.files.config import FileHandlerConfig
from pepperpy.files.types import FileMetadata


@pytest.fixture
def mock_file_path():
    """Fixture for mock file path"""
    return Path("/test/file.txt")


@pytest.fixture
def file_metadata():
    """Fixture for file metadata"""
    return FileMetadata(
        name="test.txt",
        mime_type="text/plain",
        path=Path("/test/test.txt"),
        type="text/plain",
        extension=".txt",
        format="utf-8",
        size=1024,
        metadata={"version": "1.0"},
    )


@pytest.fixture
def file_config():
    """Fixture for file config"""
    return FileHandlerConfig(
        base_path=Path("/test"),
        allowed_extensions=set([".txt", ".md"]),
        max_file_size=1024 * 1024,  # 1MB
        metadata={"environment": "test"},
    )
