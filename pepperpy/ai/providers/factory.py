"""Provider factory implementation"""

from typing import Any

from .base import BaseLLMProvider
from .openai import OpenAIConfig, OpenAIProvider
from .openrouter import OpenRouterConfig, OpenRouterProvider
from .stackspot import StackSpotConfig, StackSpotProvider

PROVIDERS = {
    "openrouter": (OpenRouterProvider, OpenRouterConfig),
    "openai": (OpenAIProvider, OpenAIConfig),
    "stackspot": (StackSpotProvider, StackSpotConfig),
}


class ProviderFactory:
    """Factory for creating LLM providers"""

    @staticmethod
    def create_provider(
        provider: str,
        api_key: str | None = None,
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs: Any,
    ) -> BaseLLMProvider:
        """Create provider instance from configuration"""
        if provider not in PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}")

        provider_class, config_class = PROVIDERS[provider]

        # Garantir que api_key não seja None
        safe_api_key = api_key or ""

        # Criar configuração específica do provider
        base_config = {
            "api_key": safe_api_key,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if provider == "openrouter":
            config = OpenRouterConfig(
                **base_config,
                generation_config={"max_tokens": max_tokens},
            )
        elif provider == "openai":
            config = OpenAIConfig(**base_config)
        elif provider == "stackspot":
            config = StackSpotConfig(
                **base_config,
                account_slug=kwargs.get("account_slug", ""),
                client_id=kwargs.get("client_id", ""),
                client_key=kwargs.get("client_key", ""),
                qc_slug=kwargs.get("qc_slug", ""),
            )
        else:
            raise ValueError(f"Provider {provider} not configured")

        return provider_class(config)
