"""Tests for embeddings client module"""

from typing import List, Sequence
from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from pepperpy.ai.embeddings.base import BaseEmbeddingProvider
from pepperpy.ai.embeddings.client import EmbeddingClient
from pepperpy.ai.embeddings.config import EmbeddingConfig
from pepperpy.ai.embeddings.exceptions import EmbeddingError
from pepperpy.ai.embeddings.types import EmbeddingResult


class MockEmbeddingProvider(BaseEmbeddingProvider):
    """Mock embedding provider for testing"""

    def __init__(self, config: EmbeddingConfig) -> None:
        """Initialize provider"""
        super().__init__(config)
        self._initialized = False
        self._model = None

    @property
    def is_initialized(self) -> bool:
        """Check if provider is initialized"""
        return self._initialized

    async def initialize(self) -> None:
        """Initialize provider"""
        self._model = Mock()
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup provider"""
        self._model = None
        self._initialized = False

    async def embed(self, text: str) -> List[float]:
        """Get embedding for text"""
        if not self._initialized:
            raise RuntimeError("Provider not initialized")

        if not text:
            raise EmbeddingError("Empty text")

        return [0.1, 0.2, 0.3]  # Test embedding

    async def embed_batch(self, texts: Sequence[str]) -> List[List[float]]:
        """Get embeddings for multiple texts"""
        if not self._initialized:
            raise RuntimeError("Provider not initialized")

        if not texts:
            raise EmbeddingError("Empty batch")

        return [[0.1, 0.2, 0.3] for _ in texts]  # Test embeddings


@pytest.fixture
def embedding_config():
    """Fixture for embedding config"""
    return EmbeddingConfig(
        model_name="test-model",
        dimension=3,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )


@pytest.fixture
def embedding_client(embedding_config):
    """Fixture for embedding client"""
    provider = MockEmbeddingProvider(embedding_config)
    return EmbeddingClient(provider)


@pytest.mark.asyncio
async def test_client_initialize(embedding_client):
    """Test client initialization"""
    await embedding_client.initialize()
    assert embedding_client.is_initialized
    assert embedding_client.provider.is_initialized


@pytest.mark.asyncio
async def test_client_cleanup(embedding_client):
    """Test client cleanup"""
    await embedding_client.initialize()
    await embedding_client.cleanup()
    assert not embedding_client.is_initialized
    assert not embedding_client.provider.is_initialized


@pytest.mark.asyncio
async def test_client_get_embedding(embedding_client):
    """Test getting embedding for text"""
    await embedding_client.initialize()

    text = "Test text"
    result = await embedding_client.embed(text)

    assert isinstance(result, EmbeddingResult)
    assert isinstance(result.embeddings, list)
    assert len(result.embeddings) == 3
    assert result.dimensions == 3
    assert result.text == text


@pytest.mark.asyncio
async def test_client_get_embeddings(embedding_client):
    """Test getting embeddings for multiple texts"""
    await embedding_client.initialize()

    texts = ["Text 1", "Text 2", "Text 3"]
    results = await embedding_client.embed_batch(texts)

    assert len(results) == 3
    for result, text in zip(results, texts):
        assert isinstance(result, EmbeddingResult)
        assert isinstance(result.embeddings, list)
        assert len(result.embeddings) == 3
        assert result.dimensions == 3
        assert result.text == text


@pytest.mark.asyncio
async def test_client_empty_text(embedding_client):
    """Test error handling for empty text"""
    await embedding_client.initialize()

    with pytest.raises(EmbeddingError, match="Empty text"):
        await embedding_client.embed("")


@pytest.mark.asyncio
async def test_client_not_initialized():
    """Test error when client not initialized"""
    config = EmbeddingConfig(
        model_name="test-model",
        dimension=3,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )
    provider = MockEmbeddingProvider(config)
    client = EmbeddingClient(provider)

    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.embed("test")


@pytest.mark.asyncio
async def test_client_provider_error(embedding_client):
    """Test error handling from provider"""
    await embedding_client.initialize()

    # Mock embed method directly
    embedding_client.provider.embed = Mock(side_effect=EmbeddingError("Provider error"))

    with pytest.raises(EmbeddingError, match="Provider error"):
        await embedding_client.embed("test")


@pytest.mark.asyncio
async def test_client_batch_processing(embedding_client):
    """Test batch processing of texts"""
    await embedding_client.initialize()

    # Test with batch size smaller than texts
    texts = [f"Text {i}" for i in range(10)]
    batch_size = 3

    results = await embedding_client.embed_batch(texts, batch_size=batch_size)

    assert len(results) == len(texts)
    for result, text in zip(results, texts):
        assert isinstance(result, EmbeddingResult)
        assert result.text == text


@pytest.mark.asyncio
async def test_client_dimension_validation():
    """Test dimension validation"""
    with pytest.raises(ValidationError) as exc_info:
        EmbeddingConfig(
            model_name="test-model",
            dimension=0,  # Invalid value
            provider_type="sentence-transformers",
        )
    assert "dimension" in str(exc_info.value)
    assert "greater than" in str(exc_info.value)


@pytest.mark.asyncio
async def test_client_model_validation():
    """Test model name validation"""
    with pytest.raises(ValueError) as exc_info:
        EmbeddingConfig(
            model_name="",  # Invalid value
            dimension=768,
            provider_type="sentence-transformers",
        )
    assert "Model name cannot be empty" in str(exc_info.value)
