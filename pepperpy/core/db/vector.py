"""Vector database configuration"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional

from ..types import JsonDict, ModuleConfig
from .config import DBConfig


@dataclass
class VectorConfig(ModuleConfig):
    """Vector database configuration"""

    name: str = "vector"
    host: str = "localhost"
    port: int = 6333
    collection: str = "vectors"
    dimension: int = 1536
    db_config: Optional[DBConfig] = None
    metadata: JsonDict = field(default_factory=dict)
    _instance: ClassVar[Any] = None

    @classmethod
    def get_default(cls) -> "VectorConfig":
        """Get default configuration instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance 