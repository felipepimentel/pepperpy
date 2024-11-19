"""Cache manager implementation"""

from dataclasses import dataclass, field
from typing import Any

from pepperpy.core.module import BaseModule, ModuleMetadata


@dataclass
class CacheManager(BaseModule):
    """Manages caching of AI responses"""

    metadata: ModuleMetadata = field(init=False)
    _cache: dict[str, Any] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        """Initialize cache manager"""
        super().__init__()
        self.metadata = ModuleMetadata(
            name="cache",
            version="1.0.0",
            description="AI response caching",
            dependencies=[],
            config={},
        )

    def get(self, key: str) -> Any:
        """Get cached value"""
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set cache value"""
        self._cache[key] = value

    def clear(self) -> None:
        """Clear cache"""
        self._cache.clear()
