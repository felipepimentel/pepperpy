"""Embedding types"""

from dataclasses import dataclass, field
from typing import Sequence

from pepperpy.core.types import JsonDict


@dataclass
class EmbeddingResult:
    """Embedding result"""

    embeddings: Sequence[float]
    model: str
    dimensions: int
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class EmbeddingBatch:
    """Batch of embeddings"""
    vectors: list[Sequence[float]]
    metadata: JsonDict = field(default_factory=dict)
