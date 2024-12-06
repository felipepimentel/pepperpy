"""Vector database configuration."""

from dataclasses import dataclass

from ..base import BaseEngineConfig


@dataclass(kw_only=True)
class VectorConfig(BaseEngineConfig):
    """Vector database configuration."""

    dimension: int
    name: str = "vector"
    host: str = "localhost"
    port: int = 6333
    collection: str = "vectors"
    index_type: str = "flat"  # flat, ivf, hnsw etc
    metric_type: str = "l2"  # l2, ip, cosine etc
    nprobe: int | None = None  # for ivf
    ef_search: int | None = None  # for hnsw
