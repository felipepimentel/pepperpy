"""Network configuration"""

from dataclasses import dataclass, field
from typing import Any, TypeVar

T = TypeVar("T")

@dataclass
class NetworkConfig:
    """Network client configuration"""

    verify_ssl: bool = True
    cert_path: str | None = None
    timeout: float = 30.0
    connect_timeout: float = 10.0
    max_retries: int = 3
    retry_backoff: float = 1.0
    max_connections: int = 100
    dns_cache_ttl: int = 10
    default_headers: dict[str, str] = field(default_factory=dict)
    cookies: dict[str, str] = field(default_factory=dict)
    _config: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: T | None = None) -> T | None:
        """Get configuration value"""
        if hasattr(self, key):
            value = getattr(self, key)
            return value if value is not None else default
        return self._config.get(key, default)
