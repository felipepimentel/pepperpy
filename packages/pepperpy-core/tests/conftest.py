"""Test configuration"""

import pytest
from pepperpy_core import BaseModule
from pydantic import BaseModel


class TestConfig(BaseModel):
    """Test configuration"""

    name: str
    value: int


class TestModule(BaseModule[TestConfig]):
    """Test module implementation"""

    async def _initialize(self) -> None:
        self._metadata["initialized"] = True

    async def _cleanup(self) -> None:
        self._metadata["cleaned"] = True


@pytest.fixture
async def test_module() -> TestModule:
    """Create test module"""
    config = TestConfig(name="test", value=42)
    return TestModule(config)
