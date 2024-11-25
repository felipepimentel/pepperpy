"""Tests for provider configuration"""

import pytest
from pydantic import ValidationError

from pepperpy.ai.providers.config import ProviderConfig
from pepperpy.ai.providers.types import ProviderType


def test_provider_config_validation():
    """Test provider config validation"""
    with pytest.raises(ValidationError):
        ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="",  # Empty API key should raise error
            model="test-model"
        )


def test_provider_config_required_fields():
    """Test required fields validation"""
    with pytest.raises(ValidationError):
        ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
            model=""
        )


def test_provider_config_valid():
    """Test valid provider config"""
    config = ProviderConfig(
        provider=ProviderType.OPENAI,
        api_key="test-key",
        model="test-model"
    )
    assert config.provider == ProviderType.OPENAI
    assert config.api_key == "test-key"
    assert config.model == "test-model"
    assert config.max_tokens == 1000  # Default value
    assert config.temperature == 0.7  # Default value
    assert config.timeout == 30.0  # Default value
    assert config.provider_options == {}  # Default value
    assert config.metadata == {}  # Default value


def test_provider_config_invalid_temperature():
    """Test invalid temperature validation"""
    with pytest.raises(ValidationError):
        ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
            model="test-model",
            temperature=2.0  # Invalid value
        )


def test_provider_config_invalid_max_tokens():
    """Test invalid max tokens validation"""
    with pytest.raises(ValidationError):
        ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
            model="test-model",
            max_tokens=0  # Invalid value
        )


def test_provider_config_invalid_timeout():
    """Test invalid timeout validation"""
    with pytest.raises(ValidationError):
        ProviderConfig(
            provider=ProviderType.OPENAI,
            api_key="test-key",
            model="test-model",
            timeout=-1  # Invalid value
        )