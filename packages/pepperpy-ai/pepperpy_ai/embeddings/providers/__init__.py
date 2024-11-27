"""Embedding providers module"""

from typing import Dict, Type

from bko.ai.embeddings.base import BaseEmbeddingProvider
from bko.ai.embeddings.config import EmbeddingConfig
from bko.ai.embeddings.exceptions import EmbeddingError

from .sentence_transformers import SentenceTransformerProvider

# Mapping of provider names to provider classes
PROVIDERS: Dict[str, Type[BaseEmbeddingProvider]] = {
    "sentence-transformers": SentenceTransformerProvider,
}


def create_provider(config: EmbeddingConfig) -> BaseEmbeddingProvider:
    """Create embedding provider from config

    Args:
        config: Provider configuration

    Returns:
        Embedding provider instance

    Raises:
        EmbeddingError: If provider type is not supported
    """
    provider_class = PROVIDERS.get(config.provider_type)
    if not provider_class:
        raise EmbeddingError(f"Unsupported provider type: {config.provider_type}")
    return provider_class(config)
