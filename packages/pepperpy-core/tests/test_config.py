"""Test configuration functionality"""

import pytest
from pydantic import BaseModel, ConfigDict

from pepperpy_core.config.manager import ConfigManager, ConfigManagerConfig


class TestConfig(BaseModel):
    """Test configuration model"""

    model_config = ConfigDict(frozen=True)

    name: str = "test"
    value: int = 42


@pytest.fixture
async def config_manager() -> ConfigManager:
    """Create config manager fixture"""
    config = ConfigManagerConfig(
        name="test", config_path="tests/data/config", enabled=True
    )
    manager = ConfigManager(config)
    await manager.initialize()
    return manager


@pytest.mark.asyncio
async def test_config_get(config_manager: ConfigManager) -> None:
    """Test config loading"""
    config = await config_manager.get_config("TestConfig", TestConfig)
    assert isinstance(config, TestConfig)
    assert config.name == "test"
    assert config.value == 42


@pytest.mark.asyncio
async def test_config_validation(config_manager: ConfigManager) -> None:
    """Test config validation"""
    with pytest.raises(ValueError):
        await config_manager.get_config("invalid_config", TestConfig)
