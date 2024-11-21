"""Embeddings module"""

from .config import EmbeddingConfig, EmbeddingProvider
from .providers import create_provider
from .types import EmbeddingResult

__all__ = [
    "EmbeddingConfig",
    "EmbeddingProvider",
    "EmbeddingResult",
    "create_provider",
]
