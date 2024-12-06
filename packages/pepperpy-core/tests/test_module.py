"""Module tests."""

from collections.abc import AsyncGenerator

import pytest

from .conftest import _TestModule


@pytest.mark.asyncio
async def test_module_initialization(
    test_module: AsyncGenerator[_TestModule, None]
) -> None:
    """Test module initialization."""
    module = await anext(test_module)
    assert module.is_initialized
    assert module.config.name == "test"
    assert module.config.enabled


@pytest.mark.asyncio
async def test_module_cleanup(test_module: AsyncGenerator[_TestModule, None]) -> None:
    """Test module cleanup."""
    module = await anext(test_module)
    await module.cleanup()
    assert not module.is_initialized


@pytest.mark.asyncio
async def test_module_stats(test_module: AsyncGenerator[_TestModule, None]) -> None:
    """Test module statistics."""
    module = await anext(test_module)
    stats = await module.get_stats()
    assert isinstance(stats, dict)
    assert "total_data" in stats
    assert "data_keys" in stats
    assert "test_value" in stats


@pytest.mark.asyncio
async def test_module_error_handling(
    test_module: AsyncGenerator[_TestModule, None]
) -> None:
    """Test module error handling."""
    module = await anext(test_module)

    # Test uninitialized state
    await module.cleanup()
    with pytest.raises(RuntimeError, match="Module not initialized"):
        await module.get_stats()
