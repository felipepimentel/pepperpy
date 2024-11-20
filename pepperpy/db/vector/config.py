"""Vector database configuration"""

from dataclasses import dataclass, field
from typing import Literal

from pepperpy.core.types import JsonDict
from pepperpy.db.config import DatabaseConfig

VectorBackend = Literal["pgvector", "faiss", "annoy"]


@dataclass
class VectorConfig:
    """Vector operations configuration"""

    db_config: DatabaseConfig
    dimension: int = 1536  # Default for OpenAI embeddings
    backend: VectorBackend = "pgvector"
    index_type: str = "ivfflat"  # pgvector specific
    distance_metric: str = "cosine"
    metadata: JsonDict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration"""
        if not isinstance(self.db_config, DatabaseConfig):
            raise ValueError("Invalid database configuration")

        if self.dimension <= 0:
            raise ValueError("Vector dimension must be positive")

        if self.backend not in ["pgvector", "faiss", "annoy"]:
            raise ValueError(f"Unsupported vector backend: {self.backend}")
