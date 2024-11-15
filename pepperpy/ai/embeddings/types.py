"""Embedding types and models"""

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray


@dataclass
class EmbeddingVector:
    """Vector representation of text"""

    vector: NDArray[np.float32]
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingBatch:
    """Batch of embedding vectors"""

    vectors: list[EmbeddingVector]
    model: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingConfig:
    """Configuration for embedding operations"""

    model: str
    provider: str
    batch_size: int = 32
    cache_enabled: bool = False
    cache_ttl: int = 3600  # 1 hour in seconds
    metadata: dict[str, Any] = field(default_factory=dict)
