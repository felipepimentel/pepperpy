from typing import AsyncGenerator

import pytest

from pepperpy.core.module import Module


class DummyModule(Module):
    """Simple test module implementation"""

    __module_name__ = "dummy"
    __version__ = "0.1.0"
    __description__ = "Test module"
    __dependencies__ = []

    async def setup(self) -> None:
        """Initialize module"""
        pass

    async def cleanup(self) -> None:
        """Cleanup module"""
        pass


@pytest.fixture
async def dummy_module() -> AsyncGenerator[DummyModule, None]:
    """Fixture providing a basic module for testing"""
    module = DummyModule()
    await module.setup()
    try:
        yield module
    finally:
        await module.cleanup()


@pytest.mark.asyncio
async def test_module_lifecycle(dummy_module: DummyModule) -> None:
    """Test basic module lifecycle"""
    assert dummy_module.__module_name__ == "dummy"
    assert dummy_module.__version__ == "0.1.0"

    health = await dummy_module.health_check()
    assert health.module == "dummy"
    assert health.status is not None
