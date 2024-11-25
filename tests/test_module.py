"""Tests for base module"""

import pytest
from pydantic import BaseModel, ConfigDict

from pepperpy.core.module import BaseModule


class TestModuleConfig(BaseModel):
    """Test module configuration"""

    model_config = ConfigDict(frozen=True)
    name: str = "test"


@pytest.fixture
def test_config():
    """Fixture for test config"""
    return TestModuleConfig()


@pytest.fixture
def test_module(test_config: TestModuleConfig):
    """Fixture for test module"""

    class TestModule(BaseModule[TestModuleConfig]):
        async def _initialize(self):
            pass

        async def _cleanup(self):
            pass

    return TestModule(test_config)
