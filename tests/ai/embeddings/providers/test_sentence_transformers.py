"""Tests for sentence transformers embedding provider"""

from unittest.mock import Mock

import numpy as np
import pytest

from pepperpy.ai.embeddings.config import EmbeddingConfig
from pepperpy.ai.embeddings.exceptions import EmbeddingError
from pepperpy.ai.embeddings.providers.sentence_transformers import SentenceTransformerProvider


@pytest.fixture
def embedding_config():
    """Fixture for embedding config"""
    return EmbeddingConfig(
        model_name="all-MiniLM-L6-v2",
        dimension=384,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )


@pytest.fixture
def mock_encode():
    """Fixture for encode method mock"""
    encode_mock = Mock()
    encode_mock.return_value = np.array([[0.1] * 384])
    return encode_mock


@pytest.fixture
def mock_model(mock_encode):
    """Fixture for model mock"""
    model_mock = Mock()
    model_mock.encode = mock_encode
    return model_mock


@pytest.fixture
def transformer_provider(embedding_config, mock_model):
    """Fixture for sentence transformer provider with mocked model"""
    provider = SentenceTransformerProvider(embedding_config)
    provider._model = mock_model  # Inject mock directly
    provider._initialized = True  # Set initialized state
    return provider


@pytest.mark.asyncio
async def test_transformer_provider_initialize(transformer_provider):
    """Test provider initialization"""
    await transformer_provider.initialize()
    assert transformer_provider.is_initialized
    assert transformer_provider.model is not None


@pytest.mark.asyncio
async def test_transformer_provider_cleanup(transformer_provider):
    """Test provider cleanup"""
    await transformer_provider.initialize()
    await transformer_provider.cleanup()
    assert not transformer_provider.is_initialized
    assert transformer_provider.model is None


@pytest.mark.asyncio
async def test_transformer_provider_not_initialized():
    """Test error when provider not initialized"""
    config = EmbeddingConfig(
        model_name="test-model", dimension=384, provider_type="sentence-transformers", metadata={}
    )
    provider = SentenceTransformerProvider(config)
    provider._initialized = False  # Garanta que está não inicializado

    with pytest.raises(RuntimeError, match="Provider not initialized"):
        await provider.embed("test")


@pytest.mark.asyncio
async def test_transformer_provider_model_error(transformer_provider):
    """Test error handling from model"""
    await transformer_provider.initialize()

    # Mock the encode method to raise an error
    mock_encode = Mock(side_effect=Exception("Model error"))
    transformer_provider._model.encode = mock_encode

    with pytest.raises(EmbeddingError) as exc_info:
        await transformer_provider.embed("test")
    assert "Failed to generate embedding" in str(exc_info.value)


@pytest.mark.asyncio
async def test_transformer_provider_dimension_mismatch(transformer_provider):
    """Test error handling for dimension mismatch"""
    await transformer_provider.initialize()

    # Mock the encode method to return wrong dimension
    mock_encode = Mock(return_value=np.array([[0.1] * 128]))  # Wrong dimension
    transformer_provider._model.encode = mock_encode

    with pytest.raises(EmbeddingError) as exc_info:
        await transformer_provider.embed("test")
    assert "Embedding dimension mismatch" in str(exc_info.value)


@pytest.mark.asyncio
async def test_transformer_provider_batch_size(transformer_provider, mock_encode):
    """Test batch size handling"""
    texts = [f"Text {i}" for i in range(10)]
    mock_encode.return_value = np.array([[0.1] * 384 for _ in range(10)])

    results = await transformer_provider.embed_batch(texts)

    assert len(results) == len(texts)
    for result in results:
        assert len(result) == transformer_provider.config.dimension


@pytest.mark.asyncio
async def test_transformer_provider_empty_text(transformer_provider):
    """Test error handling for empty text"""
    await transformer_provider.initialize()

    with pytest.raises(EmbeddingError, match="Empty text"):
        await transformer_provider.embed("")


@pytest.mark.asyncio
async def test_transformer_provider_empty_batch(transformer_provider):
    """Test error handling for empty batch"""
    await transformer_provider.initialize()

    with pytest.raises(EmbeddingError, match="Empty batch"):
        await transformer_provider.embed_batch([])
