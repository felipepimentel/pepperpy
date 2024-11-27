"""Embedding types module"""

from dataclasses import dataclass
from typing import List

# Define o tipo para vetores de embedding
EmbeddingVector = List[float]


@dataclass
class EmbeddingResult:
    """Result of embedding operation"""

    embeddings: EmbeddingVector
    dimensions: int
    text: str
    model: str

    def __len__(self) -> int:
        """Get length of embeddings"""
        return len(self.embeddings)
