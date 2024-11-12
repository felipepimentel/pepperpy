"""Embeddings configuration"""

from dataclasses import dataclass
from typing import Optional

from pepperpy.core.config import ModuleConfig


@dataclass
class EmbeddingConfig(ModuleConfig):
    """Configuration for embeddings"""

    provider: str = "sentence_transformers"
    model: str = "all-MiniLM-L6-v2"
    dimension: int = 384
    normalize: bool = True
    batch_size: int = 32
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    api_key: Optional[str] = None
