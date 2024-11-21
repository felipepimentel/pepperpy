"""Database configuration"""

from dataclasses import dataclass, field
from typing import Any, ClassVar

from ..types import JsonDict, ModuleConfig


@dataclass
class DBConfig(ModuleConfig):
    """Database configuration"""

    name: str = "db"
    host: str = "localhost"
    port: int = 5432
    database: str = "pepperpy"
    user: str = "postgres"
    password: str = ""
    metadata: JsonDict = field(default_factory=dict)
    _instance: ClassVar[Any] = None

    @classmethod
    def get_default(cls) -> "DBConfig":
        """Get default configuration instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance 