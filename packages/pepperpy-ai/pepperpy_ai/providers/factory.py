"""AI provider factory"""

from typing import Type

from ...core.exceptions import PepperPyError
from .anthropic import AnthropicProvider
from .base import BaseProvider
from .config import ProviderConfig
from .openai import OpenAIProvider
from .openrouter import OpenRouterProvider
from .stackspot import StackspotProvider


class AIProviderFactory:
    """Factory for creating AI providers"""

    _provider_map: dict[str, Type[BaseProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "openrouter": OpenRouterProvider,
        "stackspot": StackspotProvider,
    }

    @classmethod
    def create_provider(cls, config: ProviderConfig) -> BaseProvider:
        """Create provider instance"""
        try:
            if config.provider not in cls._provider_map:
                raise PepperPyError(f"Unsupported provider type: {config.provider}")

            provider_class = cls._provider_map[config.provider]
            return provider_class(config)

        except Exception as e:
            raise PepperPyError(f"Failed to create provider: {e}", cause=e)

    @classmethod
    def get_supported_providers(cls) -> list[str]:
        """Get list of supported provider types"""
        return list(cls._provider_map.keys())
