"""Security core configuration"""

from pydantic import BaseModel, ConfigDict, Field

from ...base.types import JsonDict


class SecurityConfig(BaseModel):
    """Security configuration"""

    token_expiration: int = Field(default=3600)  # 1 hour
    refresh_token_expiration: int = Field(default=86400)  # 24 hours
    algorithm: str = Field(default="HS256")
    secret_key: str = Field(default="")
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)
