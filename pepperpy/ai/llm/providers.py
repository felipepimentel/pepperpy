"""LLM provider factory"""

from typing import Optional

from .config import LLMConfig
from .exceptions import ConfigurationError
from .providers.base import BaseLLMProvider
from .providers.openai import OpenAIProvider


def get_provider(config: Optional[LLMConfig] = None) -> BaseLLMProvider:
    """Get LLM provider based on configuration"""
    if not config:
        raise ConfigurationError("LLM configuration is required")

    providers = {
        "openai": OpenAIProvider,
        # Adicione outros providers aqui
    }

    provider_class = providers.get(config.provider)
    if not provider_class:
        raise ConfigurationError(f"Unknown LLM provider: {config.provider}")

    return provider_class(config)
