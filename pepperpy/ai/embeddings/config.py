"""Embedding configuration"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from pepperpy.core.types import JsonDict


class EmbeddingProvider(str, Enum):
    """Embedding provider types"""

    OPENAI = "openai"
    HUGGINGFACE = "huggingface"
    SENTENCE_TRANSFORMERS = "sentence-transformers"
    CUSTOM = "custom"


class EmbeddingConfig(BaseModel):
    """Embedding configuration"""

    provider: EmbeddingProvider = Field(default=EmbeddingProvider.SENTENCE_TRANSFORMERS)
    model_name: str = Field(default="all-MiniLM-L6-v2")
    dimension: int = Field(default=384, gt=0)
    normalize: bool = Field(default=True)
    batch_size: int = Field(default=32, gt=0)
    provider_options: dict[str, Any] = Field(default_factory=dict)
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True

    @classmethod
    def get_default(cls) -> "EmbeddingConfig":
        """Get default configuration"""
        return cls(
            provider=EmbeddingProvider.SENTENCE_TRANSFORMERS,
            model_name="all-MiniLM-L6-v2",
            dimension=384,
            normalize=True,
            batch_size=32,
        )
