"""AI provider factory"""

from ..config import AIConfig
from ..exceptions import AIError
from .base import AIProvider
from .openai import OpenAIProvider
from .openrouter import OpenRouterProvider
from .stackspot import StackspotProvider


class AIProviderFactory:
    """Factory for creating AI providers"""

    @staticmethod
    def create_provider(config: AIConfig) -> AIProvider:
        """Create AI provider instance"""
        providers: dict[str, type[AIProvider]] = {
            "openrouter": OpenRouterProvider,
            "openai": OpenAIProvider,
            "stackspot": StackspotProvider,
        }

        provider_class = providers.get(config.provider)
        if not provider_class:
            raise AIError(f"Unknown AI provider: {config.provider}")

        return provider_class(config)
