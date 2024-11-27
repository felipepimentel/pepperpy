"""Test configuration functionality"""

import pytest
from pepperpy_core.base.types import JsonDict
from pepperpy_core.config import BaseConfig, ConfigManager, ConfigManagerConfig
from pydantic import ConfigDict, Field


class SampleTestConfig(BaseConfig):
    """Sample configuration for testing"""

    model_config = ConfigDict(frozen=True)

    name: str
    value: int
    metadata: JsonDict = Field(default_factory=dict)


@pytest.fixture
async def config_manager() -> ConfigManager:
    """Create config manager"""
    config = ConfigManagerConfig()
    manager = ConfigManager(config)
    await manager.initialize()
    yield manager
    await manager.cleanup()


async def test_load_config(config_manager: ConfigManager) -> None:
    """Test config loading"""
    data = {"name": "test", "value": 42, "metadata": {"key": "value"}}
    config = config_manager.load_config(SampleTestConfig, data)
    assert config.name == "test"
    assert config.value == 42
    assert config.metadata == {"key": "value"}
