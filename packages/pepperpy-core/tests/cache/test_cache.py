"""Test cache functionality"""

from datetime import timedelta

import pytest
from pepperpy_core.cache import CacheConfig, CacheEntry, CacheManager
from pepperpy_core.utils.datetime import utc_now


@pytest.fixture
def cache_config() -> CacheConfig:
    """Create cache configuration"""
    return CacheConfig(
        default_ttl=60,  # 1 minute
        max_size=100,
        cleanup_interval=1,  # 1 second for testing
    )


@pytest.fixture
async def cache_manager(cache_config: CacheConfig) -> CacheManager:
    """Create cache manager"""
    manager = CacheManager(cache_config)
    await manager.initialize()  # Garante inicialização
    yield manager
    await manager.cleanup()


async def test_cache_cleanup(cache_manager: CacheManager) -> None:
    """Test cache cleanup"""
    # Add expired entry
    entry = CacheEntry(
        key="test_key", value="test_value", expires_at=utc_now() - timedelta(seconds=1)
    )
    await cache_manager.set("test_key", entry)

    # Force cleanup of expired entries
    await cache_manager._cleanup()  # Usa _cleanup em vez de cleanup para não desativar o manager

    # Entry should be removed
    result = await cache_manager.get("test_key")
    assert result is None
