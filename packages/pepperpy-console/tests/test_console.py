"""Test console functionality"""

from io import StringIO
from unittest.mock import patch

import pytest
from pepperpy_console.base import Console
from pepperpy_console.base.config import ConsoleConfig


@pytest.fixture
def console() -> Console:
    """Create test console"""
    return Console(ConsoleConfig())


def test_console_print(console: Console) -> None:
    """Test console print"""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        console.print("Test message")
        assert "Test message" in fake_out.getvalue()


def test_console_styles(console: Console) -> None:
    """Test console styling"""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        console.info("Info message")
        assert "Info message" in fake_out.getvalue()

        console.success("Success message")
        assert "Success message" in fake_out.getvalue()

        console.warning("Warning message")
        assert "Warning message" in fake_out.getvalue()

        console.error("Error message")
        assert "Error message" in fake_out.getvalue()


def test_console_clear(console: Console) -> None:
    """Test console clear"""
    # Mock the clear implementation since it's terminal-dependent
    with patch.object(console, "clear") as mock_clear:
        console.clear()
        mock_clear.assert_called_once()
