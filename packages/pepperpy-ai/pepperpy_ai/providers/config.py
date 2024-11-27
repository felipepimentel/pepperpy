"""Provider configuration module"""

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProviderConfig(BaseModel):
    """Configuration for AI providers"""

    model_config = ConfigDict(frozen=True, validate_assignment=True, extra="forbid")

    provider: str = Field(..., description="Provider type")
    api_key: str = Field(..., min_length=1, description="API key for authentication")
    model: str = Field(..., min_length=1, description="Model name")
    max_tokens: int = Field(default=1000, gt=0, description="Maximum tokens per request")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Temperature for sampling")
    timeout: float = Field(default=30.0, gt=0, description="Request timeout in seconds")
    provider_options: Dict[str, Any] = Field(
        default_factory=dict, description="Provider-specific options"
    )
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate API key"""
        if not v.strip():
            raise ValueError("API key cannot be empty")
        return v

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Validate model name"""
        if not v.strip():
            raise ValueError("Model name cannot be empty")
        return v
