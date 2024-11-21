"""AI configuration"""

from typing import Any

from pydantic import BaseModel, Field

from pepperpy.core.types import JsonDict


class AIConfig(BaseModel):
    """AI configuration"""

    provider: str
    api_key: str
    model: str = Field(default="gpt-3.5-turbo")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=2048, gt=0)
    timeout: float = Field(default=30.0, gt=0)
    retry_attempts: int = Field(default=3, ge=0)
    retry_delay: float = Field(default=1.0, ge=0)
    metadata: JsonDict = Field(default_factory=dict)
    provider_options: dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True
