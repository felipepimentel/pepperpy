"""Vector operations module"""

from .client import VectorClient
from .config import VectorConfig
from .exceptions import VectorError
from .manager import VectorManager
from .types import VectorEntry, VectorQuery, VectorResult

__all__ = [
    "VectorClient",
    "VectorConfig", 
    "VectorError",
    "VectorManager",
    "VectorEntry",
    "VectorQuery",
    "VectorResult"
] 