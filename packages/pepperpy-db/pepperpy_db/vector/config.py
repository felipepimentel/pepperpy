"""Vector database configuration"""

from bko.core.types import JsonDict
from pydantic import BaseModel, Field

from ..config import DatabaseConfig


class VectorConfig(BaseModel):
    """Vector database configuration"""

    db_config: DatabaseConfig
    dimension: int = Field(default=1536, gt=0)
    index_type: str = Field(default="ivfflat")
    metric: str = Field(default="cosine")
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True
