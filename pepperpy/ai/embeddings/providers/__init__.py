"""Embedding providers package"""

from ..config import EmbeddingConfig
from ..exceptions import ConfigurationError
from .base import BaseEmbeddingProvider
from .sentence_transformers import SentenceTransformersProvider


def get_provider(config: EmbeddingConfig | None = None) -> BaseEmbeddingProvider:
    """Get embedding provider based on configuration"""
    if not config:
        raise ConfigurationError("Embedding configuration is required")

    providers = {
        "sentence_transformers": SentenceTransformersProvider,
        # Add other providers here
    }

    provider_class = providers.get(config.provider)
    if not provider_class:
        raise ConfigurationError(f"Unknown embedding provider: {config.provider}")

    return provider_class(config)


__all__ = [
    "BaseEmbeddingProvider",
    "SentenceTransformersProvider",
    "get_provider",
]
