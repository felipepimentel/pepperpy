"""Test configuration and fixtures for pepperpy-core.

Note: It's normal to have multiple conftest.py files in different test directories.
Each one provides fixtures specific to its package's tests.
"""

from dataclasses import dataclass, field
from typing import Any

import pytest

from pepperpy_core.base import BaseConfigData
from pepperpy_core.exceptions import PepperpyError
from pepperpy_core.module import BaseModule


class TestError(PepperpyError):
    """Test specific error."""

    pass


@dataclass
class TestConfig(BaseConfigData):
    """Test configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str = "test"

    # Optional fields
    enabled: bool = True
    test_data: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class TestModule(BaseModule[TestConfig]):
    """Test module implementation."""

    def __init__(self) -> None:
        """Initialize test module."""
        config = TestConfig()
        super().__init__(config)
        self._data: dict[str, Any] = {}

    async def _setup(self) -> None:
        """Setup test module."""
        pass

    async def _teardown(self) -> None:
        """Teardown test module."""
        self._data.clear()

    async def get_stats(self) -> dict[str, Any]:
        """Get test module statistics.

        Returns:
            Test module statistics
        """
        return {
            "total_data": len(self._data),
            "data_keys": list(self._data.keys()),
            "test_data": self.config.test_data,
        }


@pytest.fixture
def test_config() -> TestConfig:
    """Create test configuration.

    Returns:
        Test configuration
    """
    return TestConfig(
        name="test",
        enabled=True,
        test_data=["test1", "test2"],
    )


@pytest.fixture
async def test_module(test_config: TestConfig) -> TestModule:
    """Create and initialize test module.

    Args:
        test_config: Test configuration

    Returns:
        Initialized test module
    """
    module = TestModule()
    module.config = test_config  # Substituir a configuração padrão
    await module.initialize()
    return module
