"""LLM provider factory"""

from typing import Any, Dict, Optional, Type, Union, cast

from .config import BaseConfig, OpenAIConfig, OpenRouterConfig, ProviderType, StackSpotConfig
from .exceptions import ConfigurationError
from .providers.base import BaseLLMProvider
from .providers.openai import OpenAIProvider
from .providers.openrouter import OpenRouterProvider
from .providers.stackspot import StackSpotProvider

ProviderConfig = Union[OpenAIConfig, OpenRouterConfig, StackSpotConfig]


class ProviderFactory:
    """Factory for LLM providers"""

    _providers: Dict[ProviderType, tuple[Type[BaseLLMProvider[Any]], Type[BaseConfig]]] = {
        "openai": (OpenAIProvider, OpenAIConfig),
        "openrouter": (OpenRouterProvider, OpenRouterConfig),
        "stackspot": (StackSpotProvider, StackSpotConfig),
    }

    @classmethod
    def get_provider(
        cls, provider_type: ProviderType, config: Optional[ProviderConfig] = None
    ) -> BaseLLMProvider[Any]:
        """Get LLM provider instance

        Args:
            provider_type: Type of provider to create
            config: Provider configuration

        Returns:
            BaseLLMProvider: Provider instance

        Raises:
            ConfigurationError: If provider type is unknown or configuration is invalid
        """
        if provider_type not in cls._providers:
            raise ConfigurationError(f"Unknown provider type: {provider_type}")

        provider_class, config_class = cls._providers[provider_type]

        if config is None:
            raise ConfigurationError("Provider configuration is required")

        if not isinstance(config, config_class):
            raise ConfigurationError(
                f"Invalid configuration type for provider {provider_type}. "
                f"Expected {config_class.__name__}, got {type(config).__name__}"
            )

        provider = cast(BaseLLMProvider[Any], provider_class())
        provider.config = config
        return provider


# Convenience function
def get_provider(
    provider_type: ProviderType, config: Optional[ProviderConfig] = None
) -> BaseLLMProvider[Any]:
    """Get LLM provider instance"""
    return ProviderFactory.get_provider(provider_type, config)
