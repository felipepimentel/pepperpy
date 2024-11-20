"""Database configuration"""

from dataclasses import dataclass, field
from typing import Any, Literal

from pepperpy.core.types import JsonDict

DatabaseEngine = Literal["postgres", "mysql", "sqlite", "duckdb"]


@dataclass
class DatabaseConfig:
    """Database configuration"""

    engine: DatabaseEngine = "postgres"
    host: str = "localhost"
    port: int = 5432
    database: str = "pepperpy"
    user: str | None = None
    password: str | None = None
    ssl_mode: str | None = None
    pool_size: int = 10
    timeout: float = 30.0  # Timeout em segundos
    params: dict[str, Any] = field(default_factory=dict)  # Parâmetros específicos do engine
    metadata: JsonDict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration"""
        if self.engine not in ["postgres", "mysql", "sqlite", "duckdb"]:
            raise ValueError(f"Unsupported database engine: {self.engine}")
        
        if self.port <= 0:
            raise ValueError("Port must be positive")
        
        if self.pool_size <= 0:
            raise ValueError("Pool size must be positive")
        
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
