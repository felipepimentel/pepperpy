"""Team provider configuration"""

from typing import Any

from bko.core.types import JsonDict
from pydantic import BaseModel, Field


class TeamConfig(BaseModel):
    """Team provider configuration"""

    name: str
    enabled: bool = Field(default=True)
    max_retries: int = Field(default=3, ge=0)
    timeout: float = Field(default=60.0, gt=0)
    provider_options: dict[str, Any] = Field(default_factory=dict)
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True

    @classmethod
    def get_default(cls) -> "TeamConfig":
        """Get default configuration"""
        return cls(
            name="default",
            enabled=True,
            max_retries=3,
            timeout=60.0,
            provider_options={},
            metadata={},
        )
