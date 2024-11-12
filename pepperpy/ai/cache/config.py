"""Cache configuration"""

from dataclasses import dataclass, field
from typing import Dict

from pepperpy.core.config import ModuleConfig


@dataclass
class CacheConfig(ModuleConfig):
    """Configuration for cache"""

    default_ttl: int = 3600  # 1 hour
    max_size: int = 1000
    vector_enabled: bool = True
    vector_dimension: int = 384
    vector_similarity_threshold: float = 0.8
    cleanup_interval: int = 300  # 5 minutes
    metadata: Dict[str, str] = field(default_factory=dict)
