"""Test configuration management"""

from pathlib import Path

import pytest
from pepperpy_core.config import ConfigManager, ConfigManagerConfig


@pytest.fixture
def config_dir(tmp_path: Path) -> Path:
    """Provide temporary config directory"""
    return tmp_path / "config"


@pytest.fixture
async def config_manager(config_dir: Path) -> ConfigManager:
    """Create config manager"""
    config = ConfigManagerConfig(config_dir=config_dir)
    manager = ConfigManager(config)
    await manager.initialize()
    yield manager
    await manager.cleanup()


async def test_config_manager_initialization(config_manager: ConfigManager) -> None:
    """Test config manager initialization"""
    assert config_manager.is_initialized
    config_dir = Path(config_manager.config.config_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    assert config_dir.exists()


async def test_config_manager_settings(config_manager: ConfigManager) -> None:
    """Test config manager settings"""
    config_manager.set_config({"test_key": "test_value"})
    assert config_manager.get_config("test_key") == "test_value"
    assert config_manager.get_config("non_existent") is None
