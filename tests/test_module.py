"""Test base module implementation"""

import pytest

from pepperpy.core.dev import AsyncTestCase, async_test
from pepperpy.core.module import BaseModule, ModuleStatus
from pepperpy.core.types import JsonDict


class TestConfig:
    """Test configuration"""

    def __init__(self, name: str = "test") -> None:
        self.name = name
        self.metadata: JsonDict = {}


class TestModuleImpl(BaseModule[TestConfig]):
    """Concrete implementation for testing"""

    def __init__(self) -> None:
        super().__init__(TestConfig())

    async def _initialize(self) -> None:
        """Initialize implementation"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup implementation"""
        pass


class ErrorModuleImpl(BaseModule[TestConfig]):
    """Error module implementation"""

    def __init__(self) -> None:
        super().__init__(TestConfig())

    async def _initialize(self) -> None:
        """Initialize with error"""
        raise ValueError("Test error")

    async def _cleanup(self) -> None:
        """Cleanup implementation"""
        pass


class TestModule(AsyncTestCase):
    """Test base module"""

    @async_test
    async def test_initialization(self) -> None:
        """Test module initialization"""
        module = TestModuleImpl()
        assert module.status == ModuleStatus.UNINITIALIZED
        assert not module.is_initialized

        await module.initialize()
        assert module.status == ModuleStatus.INITIALIZED
        assert module.is_initialized

    @async_test
    async def test_cleanup(self) -> None:
        """Test module cleanup"""
        module = TestModuleImpl()
        await module.initialize()
        assert module.status == ModuleStatus.INITIALIZED

        await module.cleanup()
        assert module.status == ModuleStatus.TERMINATED
        assert not module.is_initialized

    @async_test
    async def test_error_handling(self) -> None:
        """Test module error handling"""
        module = ErrorModuleImpl()
        with pytest.raises(ValueError):
            await module.initialize()
        assert module.status == ModuleStatus.ERROR
        assert not module.is_initialized
