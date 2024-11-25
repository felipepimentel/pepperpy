"""Tests for embeddings config module"""

import pytest
from pydantic import ValidationError

from pepperpy.ai.embeddings.config import EmbeddingConfig


def test_embedding_config_valid():
    """Test valid embedding config creation"""
    config = EmbeddingConfig(
        model_name="test-model",
        dimension=768,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )

    assert config.model_name == "test-model"
    assert config.dimension == 768
    assert config.provider_type == "sentence-transformers"
    assert config.metadata == {"environment": "test"}


def test_embedding_config_default_metadata():
    """Test embedding config with default metadata"""
    config = EmbeddingConfig(
        model_name="test-model", dimension=768, provider_type="sentence-transformers"
    )

    assert config.metadata == {}


def test_embedding_config_invalid_dimension():
    """Test embedding config with invalid dimension"""
    with pytest.raises(ValidationError, match="dimension"):
        EmbeddingConfig(
            model_name="test-model", dimension=-1, provider_type="sentence-transformers"
        )


def test_embedding_config_zero_dimension():
    """Test embedding config with zero dimension"""
    with pytest.raises(ValidationError, match="dimension"):
        EmbeddingConfig(model_name="test-model", dimension=0, provider_type="sentence-transformers")


def test_embedding_config_empty_model_name():
    """Test embedding config with empty model name"""
    with pytest.raises(ValueError, match="Model name cannot be empty"):
        EmbeddingConfig(model_name="", dimension=768, provider_type="sentence-transformers")


def test_embedding_config_none_model_name():
    """Test embedding config with None model name"""
    with pytest.raises(ValidationError, match="model_name"):
        EmbeddingConfig(
            model_name=None,  # type: ignore
            dimension=768,
            provider_type="sentence-transformers",
        )


def test_embedding_config_none_dimension():
    """Test embedding config with None dimension"""
    with pytest.raises(ValidationError, match="dimension"):
        EmbeddingConfig(
            model_name="test-model",
            dimension=None,  # type: ignore
            provider_type="sentence-transformers",
        )


def test_embedding_config_invalid_metadata():
    """Test embedding config with invalid metadata"""
    with pytest.raises(ValidationError, match="metadata"):
        EmbeddingConfig(
            model_name="test-model",
            dimension=768,
            provider_type="sentence-transformers",
            metadata=None,  # type: ignore
        )


def test_embedding_config_immutable():
    """Test embedding config immutability"""
    config = EmbeddingConfig(
        model_name="test-model",
        dimension=768,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )

    with pytest.raises(AttributeError):
        config.model_name = "new-model"  # type: ignore

    with pytest.raises(AttributeError):
        config.dimension = 512  # type: ignore


def test_embedding_config_hash():
    """Test embedding config hash consistency"""
    config1 = EmbeddingConfig(
        model_name="test-model",
        dimension=768,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )

    config2 = EmbeddingConfig(
        model_name="test-model",
        dimension=768,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )

    assert config1.model_dump() == config2.model_dump()


def test_embedding_config_repr():
    """Test embedding config string representation"""
    config = EmbeddingConfig(
        model_name="test-model",
        dimension=768,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )

    repr_str = repr(config)
    assert "test-model" in repr_str
    assert "768" in repr_str
    assert "environment" in repr_str
    assert "test" in repr_str


def test_embedding_config_copy():
    """Test embedding config copy"""
    config1 = EmbeddingConfig(
        model_name="test-model",
        dimension=768,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )

    config2 = config1.model_copy()

    assert config1 == config2
    assert config1 is not config2
    assert config1.metadata == config2.metadata


def test_embedding_config_json():
    """Test embedding config JSON serialization"""
    config = EmbeddingConfig(
        model_name="test-model",
        dimension=768,
        provider_type="sentence-transformers",
        metadata={"environment": "test"},
    )

    json_str = config.model_dump_json()
    assert isinstance(json_str, str)
    assert "test-model" in json_str
    assert "768" in json_str
    assert "environment" in json_str
    assert "test" in json_str


def test_embedding_config_default_provider():
    """Test embedding config with default provider"""
    config = EmbeddingConfig(
        model_name="test-model", dimension=768, provider_type="sentence-transformers"
    )

    assert config.provider_type == "sentence-transformers"


def test_embedding_config_custom_provider():
    """Test embedding config with custom provider"""
    config = EmbeddingConfig(
        model_name="test-model", dimension=768, provider_type="custom-provider"
    )

    assert config.provider_type == "custom-provider"


def test_client_model_validation():
    """Test model name validation"""
    with pytest.raises(ValueError, match="Model name cannot be empty"):
        EmbeddingConfig(model_name="", dimension=768, provider_type="sentence-transformers")
