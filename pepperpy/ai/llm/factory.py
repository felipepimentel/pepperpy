"""LLM provider factory"""

from enum import Enum
from typing import Type

from .config import BaseConfig, OpenAIConfig, OpenRouterConfig, StackSpotConfig
from .providers import BaseLLMProvider, OpenAIProvider, OpenRouterProvider, StackSpotProvider


class ProviderType(str, Enum):
    """Available provider types"""

    OPENAI = "openai"
    OPENROUTER = "openrouter"
    STACKSPOT = "stackspot"


class ProviderFactory:
    """Factory for creating LLM providers"""

    _providers: dict[str, tuple[Type[BaseLLMProvider], Type[BaseConfig]]] = {
        ProviderType.OPENAI: (OpenAIProvider, OpenAIConfig),
        ProviderType.OPENROUTER: (OpenRouterProvider, OpenRouterConfig),
        ProviderType.STACKSPOT: (StackSpotProvider, StackSpotConfig),
    }

    @classmethod
    def get_provider(cls, provider_type: str, config: BaseConfig) -> BaseLLMProvider:
        """Get provider instance"""
        if provider_type not in cls._providers:
            raise ValueError(f"Unsupported provider type: {provider_type}")

        provider_class, config_class = cls._providers[provider_type]

        if not isinstance(config, config_class):
            raise ValueError(
                f"Invalid configuration type. Expected {config_class.__name__}, "
                f"got {type(config).__name__}"
            )

        return provider_class(config)
