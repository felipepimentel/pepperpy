"""Tests for base module functionality"""

import pytest

from pepperpy.core.base import BaseModule, ModuleConfig, ModuleStatus


class TestModule(BaseModule):
    """Test implementation of BaseModule"""

    __module_name__ = "test_module"

    async def setup(self) -> None:
        """Setup test module"""
        self._status = ModuleStatus.ACTIVE

    async def cleanup(self) -> None:
        """Cleanup test module"""
        self._status = ModuleStatus.INACTIVE


@pytest.fixture
def base_config() -> ModuleConfig:
    """Provide base module configuration"""
    return ModuleConfig(
        debug=True,
        name="test_module",
        version="1.0.0",
        timeout=30.0,
    )


@pytest.mark.asyncio
async def test_base_module_initialization(base_config):
    """Test base module initialization"""
    module = TestModule(base_config)
    assert module.get_status() == ModuleStatus.INACTIVE
    await module.setup()
    assert module.get_status() == ModuleStatus.ACTIVE


@pytest.mark.asyncio
async def test_base_module_cleanup(base_config):
    """Test base module cleanup"""
    module = TestModule(base_config)
    await module.setup()
    assert module.get_status() == ModuleStatus.ACTIVE
    await module.cleanup()
    assert module.get_status() == ModuleStatus.INACTIVE


@pytest.mark.asyncio
async def test_base_module_config(base_config):
    """Test base module configuration"""
    module = TestModule(base_config)
    assert module.config == base_config
    assert module.config.debug is True
