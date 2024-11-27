"""LLM configuration"""

from enum import Enum

from bko.core.types import JsonDict
from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """LLM provider types"""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    OPENROUTER = "openrouter"
    STACKSPOT = "stackspot"


class LLMConfig(BaseModel):
    """LLM configuration"""

    name: str
    model: str
    provider: LLMProvider
    enabled: bool = Field(default=True)
    api_key: str | None = Field(default=None)
    api_base: str | None = Field(default=None)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1000, ge=0)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0)
    presence_penalty: float = Field(default=0.0)
    stop_sequences: list[str] = Field(default_factory=list)
    timeout: float = Field(default=30.0, gt=0)
    retry_attempts: int = Field(default=3, ge=0)
    retry_delay: float = Field(default=1.0, gt=0)
    cache_enabled: bool = Field(default=True)
    cache_ttl: int = Field(default=3600)  # 1 hour
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True
