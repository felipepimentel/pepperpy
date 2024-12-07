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
    config = TestModuleConfig(name="test", enabled=True)
    module = TestModule(config)
    await module.initialize()
    try:
        yield module
    finally:
        await module.cleanup()


@pytest.mark.asyncio
async def test_module_initialization(
    test_module: AsyncGenerator[TestModule, None]
) -> None:
    """Test module initialization."""
    module = await anext(test_module)
    assert module.is_initialized
    await module.initialize()  # Should be idempotent
    assert module.is_initialized


@pytest.mark.asyncio
async def test_module_cleanup(test_module: AsyncGenerator[TestModule, None]) -> None:
    """Test module cleanup."""
    module = await anext(test_module)
    assert module.is_initialized
    await module.cleanup()
    assert not module.is_initialized


@pytest.mark.asyncio
async def test_module_stats(test_module: AsyncGenerator[TestModule, None]) -> None:
    """Test module statistics."""
    module = await anext(test_module)
    stats = await module.get_stats()
    assert isinstance(stats, dict)
    assert stats["name"] == "test"
    assert stats["total_data"] == 0
    assert stats["data_keys"] == []
    assert stats["test_value"] is None


@pytest.mark.asyncio
async def test_module_error_handling(
    test_module: AsyncGenerator[TestModule, None]
) -> None:
    """Test module error handling."""
    module = await anext(test_module)
    # Test uninitialized state
    await module.cleanup()
    assert not module.is_initialized

    # Reinitialize for cleanup
    await module.initialize()
