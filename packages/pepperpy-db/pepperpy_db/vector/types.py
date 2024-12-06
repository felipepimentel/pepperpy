"""Vector database types."""

from dataclasses import dataclass
from typing import Any


@dataclass
class VectorEntry:
    """Vector database entry."""

    id: str
    vector: list[float]
    metadata: dict[str, Any] | None = None


@dataclass
class VectorQuery:
    """Vector database query."""

    vector: list[float]
    limit: int = 10
    threshold: float | None = None


@dataclass
class VectorResult:
    """Vector database query result."""

    entry: VectorEntry
    score: float
