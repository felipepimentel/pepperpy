"""Console tests."""

import pytest

from pepperpy_console.base.console import ConsoleConfig


@pytest.fixture
def config() -> ConsoleConfig:
    """Create test config."""
    return ConsoleConfig()
