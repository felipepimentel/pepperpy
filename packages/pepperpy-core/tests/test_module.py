"""Test module functionality"""

import pytest
from pepperpy_core.base.module import BaseModule
from pepperpy_core.exceptions.module import ModuleError
from pydantic import BaseModel, ConfigDict


class SampleModuleConfig(BaseModel):
    """Sample configuration for testing"""

    model_config = ConfigDict(frozen=True)  # Usando ConfigDict em vez de Config

    name: str = "test"
    value: int = 42


class SampleTestModule(BaseModule[SampleModuleConfig]):
    """Sample module for testing"""

    async def _initialize(self) -> None:
        """Initialize module"""
        self._metadata["initialized"] = True

    async def _cleanup(self) -> None:
        """Cleanup module"""
        self._metadata["cleaned"] = True


@pytest.fixture
def module() -> SampleTestModule:
    """Create test module"""
    return SampleTestModule(SampleModuleConfig())


async def test_module_initialization(module: SampleTestModule) -> None:
    """Test module initialization"""
    assert not module.is_initialized
    await module.initialize()
    assert module.is_initialized
    assert module.metadata["initialized"]


async def test_module_cleanup(module: SampleTestModule) -> None:
    """Test module cleanup"""
    await module.initialize()
    assert module.is_initialized
    await module.cleanup()
    assert not module.is_initialized
    assert module.metadata["cleaned"]


async def test_ensure_initialized(module: SampleTestModule) -> None:
    """Test ensure initialized check"""
    with pytest.raises(ModuleError):
        module._ensure_initialized()
    await module.initialize()
    module._ensure_initialized()  # Não deve lançar erro


async def test_double_initialization(module: SampleTestModule) -> None:
    """Test double initialization"""
    await module.initialize()
    assert module.is_initialized
    await module.initialize()  # Não deve fazer nada
    assert module.is_initialized
