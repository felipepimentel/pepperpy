"""Network configuration"""

from pydantic import BaseModel, ConfigDict, Field

from ..base.types import JsonDict


class NetworkConfig(BaseModel):
    """Network configuration"""

    timeout: float = Field(default=30.0, gt=0)
    max_retries: int = Field(default=3, ge=0)
    retry_delay: float = Field(default=1.0, ge=0)
    verify_ssl: bool = Field(default=True)
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)