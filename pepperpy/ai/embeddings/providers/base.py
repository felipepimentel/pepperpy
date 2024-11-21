"""Base embedding provider"""

from abc import ABC

from pepperpy.core.module import BaseModule

from ..config import EmbeddingConfig


class EmbeddingProvider(BaseModule[EmbeddingConfig], ABC):
    """Base embedding provider implementation"""

    def __init__(self, config: EmbeddingConfig) -> None:
        """Initialize provider"""
        super().__init__(config)
