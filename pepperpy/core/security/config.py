"""Security configuration"""

from pydantic import BaseModel, Field

from pepperpy.core.types import JsonDict


class SecurityConfig(BaseModel):
    """Security configuration"""

    secret_key: str
    token_expiration: int = Field(default=3600, gt=0)  # 1 hour
    algorithm: str = Field(default="HS256")
    refresh_token_expiration: int = Field(default=604800, gt=0)  # 1 week
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True

    @classmethod
    def get_default(cls) -> "SecurityConfig":
        """Get default configuration"""
        return cls(
            secret_key="your-secret-key",
            token_expiration=3600,
            algorithm="HS256",
            refresh_token_expiration=604800,
        )
