"""Module tests"""

import pytest

from pepperpy.core.exceptions import PepperPyError
from pepperpy.core.module import InitializableModule


class TestModule(InitializableModule):
    """Test module implementation"""

    def __init__(self, should_fail: bool = False) -> None:
        super().__init__()
        self.should_fail = should_fail
        self.initialized = False
        self.cleaned_up = False

    async def _initialize(self) -> None:
        """Initialize test module"""
        if self.should_fail:
            raise PepperPyError("Initialization failed")
        self.initialized = True

    async def _cleanup(self) -> None:
        """Cleanup test module"""
        if self.should_fail:
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
    module = TestModule(should_fail=True)
    with pytest.raises(PepperPyError, match="Initialization failed"):
        await module.initialize()

    assert not module.is_initialized
    assert not module.initialized


@pytest.mark.asyncio
async def test_module_cleanup_failure() -> None:
    """Test module cleanup failure"""
    module = TestModule(should_fail=True)
    with pytest.raises(PepperPyError, match="Cleanup failed"):
        await module.cleanup()

    assert not module.cleaned_up


@pytest.mark.asyncio
async def test_ensure_initialized() -> None:
    """Test ensure initialized check"""
    module = TestModule()
    with pytest.raises(RuntimeError, match="TestModule not initialized"):
        module._ensure_initialized()

    await module.initialize()
    module._ensure_initialized()  # Should not raise
