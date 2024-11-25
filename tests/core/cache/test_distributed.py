"""Tests for distributed cache implementation"""

from unittest.mock import Mock, patch

import pytest

from pepperpy.core.cache.distributed import DistributedCache
from pepperpy.core.exceptions import PepperPyError


@pytest.fixture
def mock_redis():
    """Fixture for mock Redis client"""
    redis = Mock()
    redis.get = Mock(return_value=None)
    redis.set = Mock()
    redis.delete = Mock()
    redis.flushdb = Mock()
    redis.close = Mock()
    redis.ping = Mock()
    return redis


@pytest.fixture
def mock_redis_factory(mock_redis):
    """Fixture for mock Redis factory"""
    with patch("pepperpy.core.cache.distributed.redis.Redis") as factory:
        factory.from_url = Mock(return_value=mock_redis)
        yield factory


@pytest.fixture
def distributed_cache(mock_redis_factory):
    """Fixture for distributed cache"""
    cache = DistributedCache(
        url="redis://localhost:6379/0",
        prefix="test",
        ttl=3600
    )
    return cache


@pytest.mark.asyncio
async def test_distributed_cache_initialization(distributed_cache, mock_redis_factory):
    """Test distributed cache initialization"""
    assert not distributed_cache.is_initialized
    await distributed_cache.initialize()
    assert distributed_cache.is_initialized
    
    mock_redis_factory.from_url.assert_called_once_with(
        "redis://localhost:6379/0",
        decode_responses=True
    )


@pytest.mark.asyncio
async def test_distributed_cache_cleanup(distributed_cache, mock_redis):
    """Test distributed cache cleanup"""
    await distributed_cache.initialize()
    await distributed_cache.cleanup()
    assert not distributed_cache.is_initialized
    mock_redis.close.assert_called_once()


@pytest.mark.asyncio
async def test_distributed_cache_get(distributed_cache, mock_redis):
    """Test distributed cache get operation"""
    await distributed_cache.initialize()
    
    # Test cache miss
    mock_redis.get.return_value = None
    value = await distributed_cache.get("key1")
    assert value is None
    
    # Test cache hit
    mock_redis.get.return_value = '"value1"'
    value = await distributed_cache.get("key1")
    assert value == "value1"
    
    # Test invalid JSON
    mock_redis.get.return_value = "invalid json"
    with pytest.raises(PepperPyError, match="Failed to deserialize"):
        await distributed_cache.get("key1")


@pytest.mark.asyncio
async def test_distributed_cache_set(distributed_cache, mock_redis):
    """Test distributed cache set operation"""
    await distributed_cache.initialize()
    
    await distributed_cache.set("key1", "value1")
    mock_redis.set.assert_called_once()
    
    # Test serialization error
    class UnserializableObject:
        pass
    
    with pytest.raises(PepperPyError, match="Failed to serialize"):
        await distributed_cache.set("key2", UnserializableObject())


@pytest.mark.asyncio
async def test_distributed_cache_delete(distributed_cache, mock_redis):
    """Test distributed cache delete operation"""
    await distributed_cache.initialize()
    
    await distributed_cache.delete("key1")
    mock_redis.delete.assert_called_once_with("test:key1")


@pytest.mark.asyncio
async def test_distributed_cache_clear(distributed_cache, mock_redis):
    """Test distributed cache clear operation"""
    await distributed_cache.initialize()
    
    await distributed_cache.clear()
    mock_redis.flushdb.assert_called_once()


@pytest.mark.asyncio
async def test_distributed_cache_connection_error(mock_redis_factory):
    """Test distributed cache connection error"""
    mock_redis_factory.from_url.side_effect = Exception("Connection failed")
    
    cache = DistributedCache(url="redis://invalid-host:6379/0")
    with pytest.raises(PepperPyError, match="Failed to connect"):
        await cache.initialize()


@pytest.mark.asyncio
async def test_distributed_cache_prefix(distributed_cache, mock_redis):
    """Test distributed cache key prefixing"""
    await distributed_cache.initialize()
    
    await distributed_cache.set("key1", "value1")
    mock_redis.set.assert_called_with(
        "test:key1",
        '"value1"',
        ex=3600
    )
    
    await distributed_cache.get("key1")
    mock_redis.get.assert_called_with("test:key1")


@pytest.mark.asyncio
async def test_distributed_cache_ttl(mock_redis_factory, mock_redis):
    """Test distributed cache TTL handling"""
    cache = DistributedCache(
        url="redis://localhost:6379/0",
        ttl=1800  # 30 minutes
    )
    await cache.initialize()
    
    await cache.set("key1", "value1")
    mock_redis.set.assert_called_with(
        "test:key1",
        '"value1"',
        ex=1800
    )


@pytest.mark.asyncio
async def test_distributed_cache_no_ttl(mock_redis_factory, mock_redis):
    """Test distributed cache without TTL"""
    cache = DistributedCache(
        url="redis://localhost:6379/0",
        ttl=None
    )
    await cache.initialize()
    
    await cache.set("key1", "value1")
    mock_redis.set.assert_called_with(
        "test:key1",
        '"value1"',
        ex=None
    ) 