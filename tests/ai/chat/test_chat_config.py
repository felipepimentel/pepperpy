"""Tests for chat configuration"""


import pytest

from pepperpy.ai.chat.config import ChatConfig
from pepperpy.core.exceptions import ConfigError


def test_chat_config_creation():
    """Test chat config creation"""
    config = ChatConfig(
        model="gpt-4",
        temperature=0.7,
        max_tokens=1000,
        metadata={"language": "en"}
    )
    
    assert config.model == "gpt-4"
    assert config.temperature == 0.7
    assert config.max_tokens == 1000
    assert config.metadata == {"language": "en"}


def test_chat_config_validation():
    """Test chat config validation"""
    with pytest.raises(ValueError):
        ChatConfig(
            model="",  # Empty model should raise error
            temperature=0.7,
            max_tokens=1000
        )

    with pytest.raises(ValueError):
        ChatConfig(
            model="gpt-4",
            temperature=1.5,  # Temperature > 1.0 should raise error
            max_tokens=1000
        )

    with pytest.raises(ValueError):
        ChatConfig(
            model="gpt-4",
            temperature=0.7,
            max_tokens=-1  # Negative tokens should raise error
        )


def test_chat_config_default_values():
    """Test chat config default values"""
    config = ChatConfig(model="gpt-4")
    
    assert config.temperature == 0.7  # Default temperature
    assert config.max_tokens == 2048  # Default max tokens
    assert config.metadata == {}  # Default empty metadata


def test_chat_config_metadata_update():
    """Test chat config metadata update"""
    config = ChatConfig(
        model="gpt-4",
        metadata={"language": "en"}
    )
    
    new_metadata = {"language": "es", "style": "formal"}
    config.update_metadata(new_metadata)
    
    assert config.metadata == new_metadata


def test_chat_config_to_dict():
    """Test chat config to dictionary conversion"""
    config = ChatConfig(
        model="gpt-4",
        temperature=0.7,
        max_tokens=1000,
        metadata={"language": "en"}
    )
    
    config_dict = config.to_dict()
    
    assert isinstance(config_dict, dict)
    assert config_dict["model"] == "gpt-4"
    assert config_dict["temperature"] == 0.7
    assert config_dict["max_tokens"] == 1000
    assert config_dict["metadata"] == {"language": "en"}


def test_chat_config_from_dict():
    """Test chat config from dictionary creation"""
    config_dict = {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000,
        "metadata": {"language": "en"}
    }
    
    config = ChatConfig.from_dict(config_dict)
    
    assert config.model == "gpt-4"
    assert config.temperature == 0.7
    assert config.max_tokens == 1000
    assert config.metadata == {"language": "en"}


def test_chat_config_invalid_dict():
    """Test chat config creation from invalid dictionary"""
    with pytest.raises(ConfigError):
        ChatConfig.from_dict({})  # Empty dict should raise error

    with pytest.raises(ConfigError):
        ChatConfig.from_dict({"model": ""})  # Invalid model should raise error


def test_chat_config_string_representation():
    """Test chat config string representation"""
    config = ChatConfig(
        model="gpt-4",
        temperature=0.7,
        max_tokens=1000,
        metadata={"language": "en"}
    )
    
    expected_str = (
        "ChatConfig(model=gpt-4, temperature=0.7, "
        "max_tokens=1000, metadata={'language': 'en'})"
    )
    assert str(config) == expected_str


def test_chat_config_boundary_values():
    """Test chat config boundary values"""
    config = ChatConfig(
        model="gpt-4",
        temperature=1.0,  # Maximum valid temperature
        max_tokens=1,     # Minimum valid tokens
        metadata={}
    )
    
    assert config.temperature == 1.0
    assert config.max_tokens == 1