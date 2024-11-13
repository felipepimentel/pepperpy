"""LLM providers package"""

from typing import Optional

from ..config import LLMConfig
from ..exceptions import ConfigurationError
from .base import BaseLLMProvider
from .openai import OpenAIProvider


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


__all__ = [
    "BaseLLMProvider",
    "OpenAIProvider",
    "get_provider",
]
