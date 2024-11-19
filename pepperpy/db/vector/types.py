"""Vector database types"""

from dataclasses import dataclass, field
from typing import Sequence, TypedDict

from pepperpy.core.types import JsonDict


class VectorRow(TypedDict):
    """Database row type for vector queries"""

    id: int
    vector: list[float]
    similarity: float
    metadata: JsonDict


@dataclass
class VectorEntry:
    """Vector entry with metadata"""

    id: int
    collection: str
    vector: Sequence[float]
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class VectorQuery:
    """Vector similarity query"""

    vector: Sequence[float]
    collection: str
    limit: int = 10
    threshold: float = 0.8
    filters: JsonDict = field(default_factory=dict)


@dataclass
class VectorResult:
    """Vector similarity search result"""

    id: int
    vector: Sequence[float]
    similarity: float
    metadata: JsonDict = field(default_factory=dict)
