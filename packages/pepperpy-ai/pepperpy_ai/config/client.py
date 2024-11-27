"""AI client configuration"""

from typing import Optional

from bko.core.types import JsonDict
from pydantic import BaseModel, Field


class AIConfig(BaseModel):
    """AI configuration"""

    provider: str = Field(default="openrouter")
    model: Optional[str] = None
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=1000)
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True
