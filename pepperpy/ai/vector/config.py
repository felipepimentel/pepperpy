"""Vector configuration"""

from dataclasses import dataclass, field
from typing import Any, Literal

from pepperpy.db.config import DatabaseConfig

VectorBackend = Literal["pgvector", "faiss", "annoy"]

@dataclass
class VectorConfig:
    """Vector operations configuration"""
    
    backend: VectorBackend = "pgvector"
    dimension: int = 1536  # Default for OpenAI embeddings
    index_type: str = "ivfflat"  # pgvector specific
    distance_metric: str = "cosine"
    db_config: DatabaseConfig | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration"""
        if self.backend == "pgvector" and not self.db_config:
            raise ValueError("Database configuration required for pgvector backend") 