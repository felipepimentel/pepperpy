"""Embedding type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

import numpy as np

from pepperpy.core.types import JsonDict


@dataclass
class EmbeddingVector:
    """Vector representation of text"""

    vector: np.ndarray
    text: str
    model: str
    metadata: JsonDict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EmbeddingBatch:
    """Batch of embeddings"""

    vectors: List[EmbeddingVector]
    model: str
    metadata: JsonDict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
