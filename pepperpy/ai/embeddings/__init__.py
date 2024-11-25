"""Embeddings module"""

from .base import BaseEmbeddingProvider
from .client import EmbeddingClient
from .config import EmbeddingConfig
from .exceptions import EmbeddingError
from .providers import create_provider

__all__ = [
    "EmbeddingConfig",
    "BaseEmbeddingProvider",
    "EmbeddingClient",
    "EmbeddingError",
    "create_provider",
]
