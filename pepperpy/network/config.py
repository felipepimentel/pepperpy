"""Network configuration"""

from dataclasses import dataclass, field
from ssl import SSLContext
from typing import Dict, Optional


@dataclass
class NetworkConfig:
    """Network client configuration"""

    timeout: float = 30.0
    connect_timeout: float = 10.0
    max_retries: int = 3
    retry_backoff: float = 1.0
    verify_ssl: bool = True
    cert_path: Optional[str] = None
    max_connections: int = 100
    dns_cache_ttl: int = 10
    default_headers: Dict[str, str] = field(default_factory=dict)
    ssl_context: Optional[SSLContext] = None
