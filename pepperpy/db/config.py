"""Database configuration"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class DatabaseConfig:
    """Database configuration"""

    engine: str
    database: str
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    pool_size: int = 10
    timeout: float = 30.0
    params: Dict[str, Any] = field(default_factory=dict)
