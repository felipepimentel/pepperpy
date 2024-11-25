"""Tests for file handler base module"""

from pathlib import Path

import pytest

from pepperpy.files.config import FileHandlerConfig
from pepperpy.files.handlers.base import BaseFileHandler


@pytest.fixture
def test_handler():
    """Fixture for test handler"""
    config = FileHandlerConfig(
        base_path=Path("/test"),
        allowed_extensions={".txt"},
        max_file_size=1024 * 1024,
        metadata={"environment": "test"},
    )

    class TestHandler(BaseFileHandler):
        async def read(self, path):
            return "test"

        async def write(self, path, content):
            pass

    return TestHandler(config)
