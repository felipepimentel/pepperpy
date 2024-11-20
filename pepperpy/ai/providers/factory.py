"""Provider factory implementation"""

from typing import Any

from ..llm.config import LLMConfig, LLMProvider
from .exceptions import ProviderError
from .openrouter import OpenRouterProvider


class ProviderFactory:
    """Factory for creating providers"""

    @staticmethod
    def create_provider(config: LLMConfig, **kwargs: Any) -> Any:
        """Create provider instance.
        
        Args:
            config: LLM configuration
            **kwargs: Additional arguments
            
        Returns:
            Provider instance
            
        Raises:
            ProviderError: If provider is not supported
        """
        try:
            providers = {
                LLMProvider.OPENROUTER: OpenRouterProvider,
                # Adicionar outros providers conforme necessário
            }

            provider_class = providers.get(config.provider)
            if not provider_class:
                raise ProviderError(f"Unsupported provider: {config.provider}")

            return provider_class(config, **kwargs)

        except Exception as e:
            raise ProviderError(f"Failed to create provider: {e}", cause=e)
