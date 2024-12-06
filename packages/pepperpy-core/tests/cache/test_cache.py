"""Cache tests."""

from collections.abc import AsyncGenerator
from typing import Any

import pytest

from pepperpy_core.cache import BaseCache, CacheConfig, CacheEntry


class TestCache(BaseCache[CacheConfig]):
    """Test cache implementation."""

    def __init__(self, config: CacheConfig) -> None:
        """Initialize cache."""
        super().__init__(config)
        self._data: dict[str, CacheEntry] = {}

    async def _setup(self) -> None:
        """Setup cache resources."""
        self._data = {}

    async def _teardown(self) -> None:
        """Teardown cache resources."""
        self._data.clear()

    async def get(self, key: str) -> Any:
        """Get value from cache."""
        entry = self._data.get(key)
        if entry is None:
            return None
        return entry.value

    async def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        import time

        entry = CacheEntry(
            key=key, value=value, expires_at=time.time() + self.config.ttl
        )
        self._data[key] = entry

    async def delete(self, key: str) -> None:
        """Delete value from cache."""
        self._data.pop(key, None)

    async def clear(self) -> None:
        """Clear all values from cache."""
        self._data.clear()


@pytest.fixture
def cache_config() -> CacheConfig:
    """Create test cache config.

    Returns:
        Test cache configuration
    """
    return CacheConfig(
        name="test_cache",
        ttl=60,
        max_size=100,
    )


@pytest.fixture
async def cache(
    cache_config: CacheConfig,
) -> AsyncGenerator[BaseCache[CacheConfig], None]:
    """Create test cache.

    Args:
        cache_config: Cache configuration

    Returns:
        Test cache instance
    """
    cache = TestCache(cache_config)
    await cache.initialize()
    yield cache
    await cache.cleanup()


@pytest.mark.asyncio
async def test_cache_operations(cache: BaseCache[CacheConfig]) -> None:
    """Test basic cache operations."""
    # Test set
    await cache.set("test", "value")

    # Test get
    result = await cache.get("test")
    assert result == "value"

    # Test delete
    await cache.delete("test")
    result = await cache.get("test")
    assert result is None

    # Test clear
    await cache.set("test1", "value1")
    await cache.set("test2", "value2")
    await cache.clear()
    result1 = await cache.get("test1")
    result2 = await cache.get("test2")
    assert result1 is None
    assert result2 is None
