"""Vector database types"""

from dataclasses import dataclass, field
from typing import Sequence, TypedDict

from pydantic import BaseModel, Field, confloat, conint

from pepperpy.core.types import JsonDict


class VectorQuery(BaseModel):
    """Vector similarity query"""

    vector: list[float]
    collection: str
    limit: conint(gt=0) = Field(default=10)  # type: ignore
    threshold: confloat(ge=0, le=1) = Field(default=0.8)  # type: ignore
    filters: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True


@dataclass
class VectorResult:
    """Vector similarity search result"""

    id: int
    vector: Sequence[float]
    similarity: float
    metadata: JsonDict = field(default_factory=dict)


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
