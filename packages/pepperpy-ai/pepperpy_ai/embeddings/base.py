"""Base embedding provider implementation"""

from abc import ABC, abstractmethod
from typing import Generic, List, Sequence, TypeVar

from pydantic import BaseModel

from ..base.module import BaseModule

ConfigT = TypeVar("ConfigT", bound=BaseModel)


class EmbeddingProvider(BaseModule[ConfigT], Generic[ConfigT], ABC):
    """Base embedding provider interface"""

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Get embedding for text"""
        ...

    @abstractmethod
    async def embed_batch(self, texts: Sequence[str]) -> List[List[float]]:
        """Get embeddings for multiple texts"""
        ...

    async def _initialize(self) -> None:
        """Initialize provider implementation"""
        ...

    async def _cleanup(self) -> None:
        """Cleanup provider implementation"""
        ...


__all__ = [
    "EmbeddingProvider",
]
