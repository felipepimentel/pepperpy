"""Configuration manager tests."""

import json
import os
import shutil
from collections.abc import AsyncGenerator, Generator
from pathlib import Path

import pytest
from pepperpy_core.config import ConfigManager
from pepperpy_core.config.types import ConfigManagerConfig
from pydantic import BaseModel


class _TestConfig(BaseModel):
    """Test configuration model."""

    name: str = "test"
    value: str = "test_value"


@pytest.fixture
def test_config_dir() -> str:
    """Create and return a test config directory."""
    config_dir = "/tmp/test_config"
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


@pytest.fixture
def manager_config(test_config_dir: str) -> ConfigManagerConfig:
    """Create test configuration."""
    return ConfigManagerConfig(
        name="test_manager",
        config_path=test_config_dir,
        enabled=True,
    )


@pytest.fixture
async def manager(
    manager_config: ConfigManagerConfig,
) -> AsyncGenerator[ConfigManager, None]:
    """Create config manager fixture."""
    manager = ConfigManager(config=manager_config)
    await manager.initialize()
    try:
        yield manager
    finally:
        await manager.cleanup()


async def test_manager_initialization(manager: ConfigManager) -> None:
    """Test manager initialization."""
    # Initialize should be idempotent
    await manager.initialize()
    await manager.initialize()  # Second call should be no-op

    # Verify manager is ready for use
    assert await manager.is_ready()


async def test_manager_cleanup(manager: ConfigManager) -> None:
    """Test manager cleanup."""
    await manager.initialize()
    await manager.cleanup()

    # Verify manager is cleaned up
    assert not await manager.is_ready()


@pytest.mark.asyncio
async def test_basic_operations(manager: ConfigManager) -> None:
    """Test basic configuration operations."""
    assert await manager.is_ready()

    # Test cleanup
    await manager.cleanup()
    assert not await manager.is_ready()


@pytest.mark.asyncio
async def test_config_get(
    manager: ConfigManager,
    test_config_dir: str,
) -> None:
    """Test config loading."""
    # Create a test config file
    config_path = Path(test_config_dir) / "test_config.json"
    config_path.write_text(json.dumps({"name": "test", "value": "test_value"}))

    config = await manager.get_config("test_config", _TestConfig)
    assert config is not None
    assert isinstance(config, _TestConfig)
    assert config.name == "test"
    assert config.value == "test_value"


@pytest.mark.asyncio
async def test_config_validation(
    manager: ConfigManager,
    test_config_dir: str,
) -> None:
    """Test config validation."""
    # Ensure the config file doesn't exist
    config_path = Path(test_config_dir) / "invalid_config.json"
    if config_path.exists():
        config_path.unlink()

    with pytest.raises(ValueError, match="Config file not found: invalid_config"):
        await manager.get_config("invalid_config", _TestConfig)


@pytest.fixture(autouse=True)
def cleanup_test_files(test_config_dir: str) -> Generator[None, None, None]:
    """Clean up test files after each test."""
    yield
    shutil.rmtree(test_config_dir, ignore_errors=True)
