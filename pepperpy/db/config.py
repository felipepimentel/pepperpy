"""Database configuration"""

from typing import Any

from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    """Database configuration"""

    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    database: str
    user: str
    password: str
    pool_size: int = Field(default=10)
    min_size: int = Field(default=1)
    max_size: int = Field(default=20)
    timeout: float = Field(default=60.0)
    params: dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True
