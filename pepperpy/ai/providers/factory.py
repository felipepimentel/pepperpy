"""AI provider factory implementation"""

from ..config.provider import ProviderConfig
from .base import AIProvider
from .openai import OpenAIProvider
from .openrouter import OpenRouterProvider


class AIProviderFactory:
    """Factory for creating AI providers"""

    @staticmethod
    def create_provider(config: ProviderConfig) -> AIProvider:
        """Create an AI provider based on the configuration"""
        if config.provider == "openai":
            return OpenAIProvider(config)
        elif config.provider == "openrouter":
            return OpenRouterProvider(config)
        else:
            raise ValueError(f"Unknown AI provider: {config.provider}")
