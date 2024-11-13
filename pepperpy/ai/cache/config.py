"""Cache configuration"""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict


@dataclass
class CacheConfig:
    """Configuration for cache operations"""

    enabled: bool = True
    ttl: int = 3600  # Time to live in seconds
    max_size: int = 1000  # Maximum number of items
    strategy: str = "lru"  # Cache eviction strategy
    namespace: str = "default"  # Cache namespace
    metadata: Dict[str, Any] = field(default_factory=dict)

    def dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self)
