"""Cache type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, TypeAlias, Union

# Type aliases
CacheKey: TypeAlias = str
CacheValue: TypeAlias = Union[str, bytes, int, float, bool, dict, list, None]


@dataclass
class CacheEntry:
    """Cache entry data"""

    key: CacheKey
    value: CacheValue
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        """Check if entry is expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "key": self.key,
            "value": self.value,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CacheEntry":
        """Create from dictionary"""
        expires_at = data.get("expires_at")
        if expires_at:
            expires_at = datetime.fromisoformat(expires_at)

        return cls(
            key=data["key"],
            value=data["value"],
            expires_at=expires_at,
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata", {}),
        )
