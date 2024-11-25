"""Tests for cache base module"""

import pytest

from pepperpy.core.cache.base import BaseCache, CacheProvider


@pytest.fixture
def test_cache():
    """Fixture for test cache"""

    class TestCache(BaseCache):
        async def get(self, key: str) -> str:
            return "test"

        async def set(self, key: str, value: str) -> None:
            pass

        async def delete(self, key: str) -> None:
            pass

        async def clear(self) -> None:
            pass

        async def _initialize(self) -> None:
            pass

        async def _cleanup(self) -> None:
            pass

    return TestCache()


@pytest.fixture
def test_provider():
    """Fixture for test provider"""

    class TestProvider(CacheProvider):
        async def get_cache(self) -> BaseCache:
            return test_cache()

        async def create_cache(self) -> BaseCache:
            """Create a new cache instance"""
            return test_cache()

        async def delete_cache(self) -> None:
            """Delete the cache instance"""
            pass

        async def _initialize(self) -> None:
            pass

        async def _cleanup(self) -> None:
            pass

    return TestProvider()
