"""LLM factory implementation"""

from typing import Any

from .client import LLMClient
from .config import LLMConfig, LLMProvider
from .exceptions import LLMError


class LLMFactory:
    """Factory for creating LLM clients"""

    @staticmethod
    def create_client(config: LLMConfig, **kwargs: Any) -> LLMClient:
        """Create LLM client instance.
        
        Args:
            config: LLM configuration
            **kwargs: Additional arguments
            
        Returns:
            LLMClient: Configured LLM client
            
        Raises:
            LLMError: If provider is not supported
        """
        try:
            return LLMClient(config)
        except Exception as e:
            raise LLMError(f"Failed to create LLM client: {e}", cause=e)

    @staticmethod
    def create_config(
        name: str,
        provider: str | LLMProvider,
        model: str,
        **kwargs: Any
    ) -> LLMConfig:
        """Create LLM configuration.
        
        Args:
            name: Configuration name
            provider: LLM provider name or enum
            model: Model name
            **kwargs: Additional configuration options
            
        Returns:
            LLMConfig: LLM configuration
            
        Raises:
            LLMError: If provider is not supported
        """
        try:
            if isinstance(provider, str):
                provider = LLMProvider(provider)
            return LLMConfig(
                name=name,
                provider=provider,
                model=model,
                **kwargs
            )
        except Exception as e:
            raise LLMError(f"Failed to create LLM config: {e}", cause=e)
