"""Tests for AI cache"""

from unittest.mock import AsyncMock

import pytest

from pepperpy.ai.cache import AICache
from pepperpy.ai.types import AIMessage, AIResponse, MessageRole
from pepperpy.core.cache.base import BaseCache
from pepperpy.core.exceptions import PepperPyError


class MockCache(BaseCache):
    """Mock cache implementation"""

    def __init__(self) -> None:
        self.store: dict = {}
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize cache"""
        await self._initialize()

    async def cleanup(self) -> None:
        """Cleanup cache"""
        await self._cleanup()

    async def _initialize(self) -> None:
        """Initialize cache"""
        self._initialized = True

    async def _cleanup(self) -> None:
        """Cleanup cache"""
        self.store.clear()
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if cache is initialized"""
        return self._initialized

    async def get(self, key: str) -> AIResponse | None:
        """Get value from cache"""
        if not self.is_initialized:
            raise RuntimeError("Cache not initialized")
        return self.store.get(key)

    async def set(self, key: str, value: AIResponse) -> None:
        """Set value in cache"""
        if not self.is_initialized:
            raise RuntimeError("Cache not initialized")
        self.store[key] = value

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        if not self.is_initialized:
            raise RuntimeError("Cache not initialized")
        self.store.pop(key, None)

    async def clear(self) -> None:
        """Clear cache"""
        if not self.is_initialized:
            raise RuntimeError("Cache not initialized")
        self.store.clear()


@pytest.fixture
def mock_cache():
    """Fixture for mock cache"""
    return MockCache()


@pytest.fixture
def ai_cache(mock_cache):
    """Fixture for AI cache"""
    return AICache(mock_cache)


@pytest.fixture
def sample_response():
    """Fixture for sample AI response"""
    return AIResponse(
        content="Test response",
        messages=[AIMessage(role=MessageRole.ASSISTANT, content="Test response")]
    )


@pytest.mark.asyncio
async def test_cache_initialization(ai_cache):
    """Test cache initialization"""
    assert not ai_cache.is_initialized
    await ai_cache.initialize()
    assert ai_cache.is_initialized


@pytest.mark.asyncio
async def test_cache_cleanup(ai_cache):
    """Test cache cleanup"""
    await ai_cache.initialize()
    await ai_cache.cleanup()
    assert not ai_cache.is_initialized


@pytest.mark.asyncio
async def test_cache_get_set(ai_cache, sample_response):
    """Test cache get and set operations"""
    await ai_cache.initialize()
    
    key = "test_key"
    await ai_cache.set(key, sample_response)
    
    cached = await ai_cache.get(key)
    assert cached is not None
    assert cached.content == sample_response.content
    assert cached.messages == sample_response.messages


@pytest.mark.asyncio
async def test_cache_delete(ai_cache, sample_response):
    """Test cache delete operation"""
    await ai_cache.initialize()
    
    key = "test_key"
    await ai_cache.set(key, sample_response)
    await ai_cache.delete(key)
    
    cached = await ai_cache.get(key)
    assert cached is None


@pytest.mark.asyncio
async def test_cache_clear(ai_cache, sample_response):
    """Test cache clear operation"""
    await ai_cache.initialize()
    
    keys = ["key1", "key2", "key3"]
    for key in keys:
        await ai_cache.set(key, sample_response)
    
    await ai_cache.clear()
    
    for key in keys:
        cached = await ai_cache.get(key)
        assert cached is None


@pytest.mark.asyncio
async def test_cache_not_initialized_error(ai_cache):
    """Test error when cache not initialized"""
    with pytest.raises(PepperPyError, match="Cache operation failed"):
        await ai_cache.get("test_key")


@pytest.mark.asyncio
async def test_cache_key_generation(ai_cache):
    """Test cache key generation"""
    prompt = "Test prompt"
    model = "test-model"
    key1 = ai_cache.generate_key(prompt, model=model)
    key2 = ai_cache.generate_key(prompt, model=model)
    
    assert key1 == key2
    assert isinstance(key1, str)
    assert len(key1) > 0


@pytest.mark.asyncio
async def test_cache_with_different_params(ai_cache, sample_response):
    """Test cache with different parameters"""
    await ai_cache.initialize()
    
    prompt = "Test prompt"
    key1 = ai_cache.generate_key(prompt, model="model1")
    key2 = ai_cache.generate_key(prompt, model="model2")
    
    await ai_cache.set(key1, sample_response)
    cached1 = await ai_cache.get(key1)
    cached2 = await ai_cache.get(key2)
    
    assert cached1 is not None
    assert cached2 is None


@pytest.mark.asyncio
async def test_cache_error_handling(ai_cache):
    """Test cache error handling"""
    await ai_cache.initialize()
    
    # Simulate cache error
    ai_cache._cache.get = AsyncMock(side_effect=Exception("Cache error"))
    
    with pytest.raises(PepperPyError, match="Cache operation failed"):
        await ai_cache.get("test_key") 