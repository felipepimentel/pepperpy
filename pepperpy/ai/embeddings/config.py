"""Embedding configuration"""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict


@dataclass
class EmbeddingConfig:
    """Configuration for embedding operations"""

    model: str
    provider: str
    batch_size: int = 32
    cache_enabled: bool = False
    cache_ttl: int = 3600  # 1 hour in seconds
    metadata: Dict[str, Any] = field(default_factory=dict)

    def dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self)