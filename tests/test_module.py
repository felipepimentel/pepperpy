"""Test base module functionality"""

from dataclasses import asdict

import pytest

from pepperpy.core.config import ModuleConfig
from pepperpy.core.module import BaseModule, ModuleStatus


class DummyModule(BaseModule):
    """Test implementation of BaseModule"""

    __module_name__ = "test_module"

    async def _setup(self) -> None:
        """Setup test module"""
        self._status = ModuleStatus.ACTIVE

    async def _cleanup(self) -> None:
        """Cleanup test module"""
        self._status = ModuleStatus.INACTIVE


@pytest.fixture
def base_config() -> ModuleConfig:
    """Provide base module configuration"""
    return ModuleConfig(
        name="test_module",
        version="1.0.0",
        debug=True,
    )


@pytest.mark.asyncio
async def test_base_module_initialization(base_config: ModuleConfig):
    """Test base module initialization"""
    module = DummyModule()
    module.config = asdict(base_config)
    assert module.status == ModuleStatus.INACTIVE
    await module.initialize()
    assert module.status == ModuleStatus.ACTIVE


@pytest.mark.asyncio
async def test_base_module_cleanup(base_config: ModuleConfig):
    """Test base module cleanup"""
    module = DummyModule()
    module.config = asdict(base_config)
    await module.initialize()
    assert module.status == ModuleStatus.ACTIVE
    await module.cleanup()
    assert module.status == ModuleStatus.INACTIVE


@pytest.mark.asyncio
async def test_base_module_config(base_config: ModuleConfig):
    """Test base module configuration"""
    module = DummyModule()
    config_dict = asdict(base_config)
    module.config = config_dict
    assert module.config == config_dict
    assert module.config["debug"] is True
