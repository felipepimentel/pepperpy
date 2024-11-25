"""Embedding configuration module"""

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EmbeddingConfig(BaseModel):
    """Configuration for embedding operations"""

    model_config = ConfigDict(frozen=True, validate_assignment=True, extra="forbid")

    model_name: str = Field(..., description="Name of the model to use")
    dimension: int = Field(..., gt=0, description="Embedding dimension")
    provider_type: str = Field("sentence-transformers", description="Type of embedding provider")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Validate model name"""
        if not v:
            raise ValueError("Model name cannot be empty")
        return v
