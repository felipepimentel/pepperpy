"""Test module functionality."""

from collections.abc import AsyncGenerator
from typing import Any

import pytest
from pepperpy_core.base import BaseConfigData, BaseModule


class TestModuleConfig(BaseConfigData):
    """Test module configuration."""

    name: str = "test"


class TestModule(BaseModule[TestModuleConfig]):
    """Test module implementation."""

    async def _setup(self) -> None:
        """Setup test module."""
        pass

    async def _teardown(self) -> None:
        """Teardown test module."""
        pass

    async def get_stats(self) -> dict[str, Any]:
        """Get test module statistics."""
        return {
            "name": self.config.name,
            "total_data": 0,
            "data_keys": [],
            "test_value": None,
        }


@pytest.fixture
async def test_module() -> AsyncGenerator[TestModule, None]:
    """Create test module fixture."""
    config = TestModuleConfig(name="test")
    module = TestModule(config)
    await module.initialize()
    try:
        yield module
    finally:
        await module.cleanup()


@pytest.mark.asyncio
async def test_module_initialization(test_module: TestModule) -> None:
    """Test module initialization."""
    assert test_module.is_initialized
    assert test_module.config.name == "test"
    assert test_module.config.enabled


@pytest.mark.asyncio
async def test_module_cleanup(test_module: TestModule) -> None:
    """Test module cleanup."""
    await test_module.cleanup()
    assert not test_module.is_initialized


@pytest.mark.asyncio
async def test_module_stats(test_module: TestModule) -> None:
    """Test module statistics."""
    stats = await test_module.get_stats()
    assert isinstance(stats, dict)
    assert "total_data" in stats
    assert "data_keys" in stats
    assert "test_value" in stats


@pytest.mark.asyncio
async def test_module_error_handling(test_module: TestModule) -> None:
    """Test module error handling."""

    # Test uninitialized state
    await test_module.cleanup()
    with pytest.raises(RuntimeError, match="Module not initialized"):
        await test_module.get_stats()
