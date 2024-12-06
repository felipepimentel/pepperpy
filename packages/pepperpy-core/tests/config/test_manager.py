"""Test configuration manager."""

import pytest
from pydantic import BaseModel

from pepperpy_core.config.manager import ConfigManager, ConfigManagerConfig


class TestConfigModel(BaseModel):
    """Test configuration model."""

    key: str = "value"


@pytest.fixture
def config() -> ConfigManagerConfig:
    """Create test configuration.

    Returns:
        Test configuration manager config
    """
    return ConfigManagerConfig(
        name="test_config", config_path="/tmp/test_config", enabled=True
    )


@pytest.fixture
async def config_manager(config: ConfigManagerConfig) -> ConfigManager:
    """Create test configuration manager.

    Args:
        config: Configuration manager config

    Returns:
        Initialized configuration manager
    """
    manager = ConfigManager(config)
    await manager.initialize()
    return manager


@pytest.mark.asyncio
async def test_basic_operations(config_manager: ConfigManager) -> None:
    """Test basic configuration operations."""
    # Test initialization
    assert config_manager._initialized  # Usando atributo interno
    assert config_manager.config.config_path == "/tmp/test_config"

    # Test get_config
    config = await config_manager.get_config("test", TestConfigModel)
    assert isinstance(config, TestConfigModel)
    assert config.key == "value"

    # Test missing config
    config = await config_manager.get_config("missing", TestConfigModel)
    assert config is None


@pytest.mark.asyncio
async def test_cleanup(config_manager: ConfigManager) -> None:
    """Test configuration manager cleanup."""
    await config_manager.cleanup()
    assert not config_manager._initialized
