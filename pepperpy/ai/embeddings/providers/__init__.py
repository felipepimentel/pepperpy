"""Embedding providers module"""

from typing import Type

from ...exceptions import AIError
from ..config import EmbeddingConfig, EmbeddingProvider
from .base import EmbeddingProvider as BaseProvider
from .huggingface import HuggingFaceProvider
from .openai import OpenAIProvider
from .sentence_transformers import SentenceTransformersProvider

__all__ = [
    "EmbeddingProvider",
    "BaseProvider",
    "create_provider",
]

_PROVIDERS: dict[EmbeddingProvider, Type[BaseProvider]] = {
    EmbeddingProvider.OPENAI: OpenAIProvider,
    EmbeddingProvider.HUGGINGFACE: HuggingFaceProvider,
    EmbeddingProvider.SENTENCE_TRANSFORMERS: SentenceTransformersProvider,
}


def create_provider(config: EmbeddingConfig) -> BaseProvider:
    """Create embedding provider instance"""
    provider_class = _PROVIDERS.get(config.provider)
    if not provider_class:
        raise AIError(f"Unknown embedding provider: {config.provider}")
    return provider_class(config=config)
