"""Configuration manager tests."""

import json
import os
import shutil
from collections.abc import AsyncGenerator, Generator
from pathlib import Path

import pytest
from pydantic import BaseModel

from pepperpy_core.config import ConfigManager
from pepperpy_core.config.types import ConfigManagerConfig


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
async def config_manager(
    manager_config: ConfigManagerConfig,
) -> AsyncGenerator[ConfigManager, None]:
    """Create config manager fixture."""
    manager = ConfigManager(config=manager_config)
    await manager.initialize()
    try:
        yield manager
    finally:
        await manager.cleanup()


@pytest.mark.asyncio
async def test_basic_operations(
    config_manager: AsyncGenerator[ConfigManager, None]
) -> None:
    """Test basic configuration operations."""
    manager = await anext(config_manager)
    assert manager._initialized

    # Test cleanup
    await manager.cleanup()
    assert not manager._initialized


@pytest.mark.asyncio
async def test_config_get(
    config_manager: AsyncGenerator[ConfigManager, None],
    test_config_dir: str,
) -> None:
    """Test config loading."""
    manager = await anext(config_manager)

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
    config_manager: AsyncGenerator[ConfigManager, None],
    test_config_dir: str,
) -> None:
    """Test config validation."""
    manager = await anext(config_manager)

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
