"""Module tests"""

import pytest
from pydantic import BaseModel

from pepperpy.core.exceptions import PepperPyError
from pepperpy.core.module import BaseModule


class TestModuleConfig(BaseModel):
    """Test module configuration"""

    should_fail_init: bool = False
    should_fail_cleanup: bool = False


class TestModule(BaseModule[TestModuleConfig]):
    """Test module implementation"""

    def __init__(self, should_fail_init: bool = False, should_fail_cleanup: bool = False) -> None:
        config = TestModuleConfig(
            should_fail_init=should_fail_init, should_fail_cleanup=should_fail_cleanup
        )
        super().__init__(config)
        self.initialized = False
        self.cleaned_up = False

    async def _initialize(self) -> None:
        """Initialize module"""
        if self.config.should_fail_init:
            raise PepperPyError("Initialization failed")
        self.initialized = True

    async def _cleanup(self) -> None:
        """Cleanup module"""
        if self.config.should_fail_cleanup:
            raise PepperPyError("Cleanup failed")
        self.cleaned_up = True


@pytest.mark.asyncio
async def test_module_initialization() -> None:
    """Test module initialization"""
    module = TestModule()
    assert not module.is_initialized
    assert not module.initialized

    await module.initialize()
    assert module.is_initialized
    assert module.initialized

    await module.cleanup()
    assert not module.is_initialized
    assert module.cleaned_up


@pytest.mark.asyncio
async def test_module_initialization_failure() -> None:
    """Test module initialization failure"""
    module = TestModule(should_fail_init=True)
    with pytest.raises(PepperPyError, match="Initialization failed"):
        await module.initialize()

    assert not module.is_initialized
    assert not module.initialized


@pytest.mark.asyncio
async def test_module_cleanup_failure() -> None:
    """Test module cleanup failure"""
    module = TestModule(should_fail_cleanup=True)
    await module.initialize()  # Não vai falhar pois só falha no cleanup

    with pytest.raises(PepperPyError) as exc_info:
        await module.cleanup()

    assert str(exc_info.value) == "Cleanup failed"
    assert not module.cleaned_up


@pytest.mark.asyncio
async def test_ensure_initialized() -> None:
    """Test ensure initialized check"""
    module = TestModule()
    with pytest.raises(RuntimeError, match="TestModule not initialized"):
        module._ensure_initialized()

    await module.initialize()
    module._ensure_initialized()  # Should not raise
