"""Module tests."""

import pytest

from .conftest import TestConfig, TestModule


async def test_module_initialization(test_module: TestModule) -> None:
    """Test module initialization."""
    assert test_module.is_initialized
    assert test_module.config.name == "test"
    assert test_module.config.enabled


async def test_module_cleanup(test_module: TestModule) -> None:
    """Test module cleanup."""
    await test_module.cleanup()
    assert not test_module.is_initialized


async def test_module_stats(test_module: TestModule) -> None:
    """Test module statistics."""
    stats = await test_module.get_stats()
    assert isinstance(stats, dict)
    assert "total_data" in stats
    assert "data_keys" in stats
    assert "test_data" in stats


async def test_module_error_handling(test_config: TestConfig) -> None:
    """Test module error handling."""
    module = TestModule()
    module.config = test_config

    with pytest.raises(RuntimeError):
        await module.get_stats()

    await module.initialize()
    assert module.is_initialized

    await module.cleanup()
    with pytest.raises(RuntimeError):
        await module.get_stats()
