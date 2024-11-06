from typing import AsyncGenerator

import pytest

from pepperpy.core.module import Module
from pepperpy.core.types import Status


class DummyModule(Module):
    """Simple test module implementation"""

    __module_name__ = "dummy"
    __version__ = "0.1.0"
    __description__ = "Test module"
    __dependencies__ = []

    async def setup(self) -> None:
        """Initialize module"""
        self._status = Status.ACTIVE

    async def cleanup(self) -> None:
        """Cleanup module"""
        self._status = Status.INACTIVE


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
    # Test module metadata
    assert dummy_module.__module_name__ == "dummy"
    assert dummy_module.__version__ == "0.1.0"

    # Test health check
    health = await dummy_module.health_check()
    assert health.module == "dummy"
    assert health.state == Status.ACTIVE

    # Test health details
    assert health.details["version"] == "0.1.0"
    assert health.details["status"] == Status.ACTIVE

    # Test cleanup
    await dummy_module.cleanup()
    health = await dummy_module.health_check()
    assert health.state == Status.INACTIVE
