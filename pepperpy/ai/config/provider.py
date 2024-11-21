"""AI provider configuration"""

import os
from typing import Any, Literal

from pydantic import BaseModel, Field

from pepperpy.core.types import JsonDict

ProviderType = Literal["openai", "anthropic", "openrouter", "stackspot"]


class ProviderConfig(BaseModel):
    """AI provider configuration"""

    provider: ProviderType
    api_key: str = Field(default="")
    model: str = Field(default="gpt-3.5-turbo")
    max_tokens: int = Field(default=1000, ge=0)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    timeout: float = Field(default=30.0, gt=0)
    provider_options: dict[str, Any] = Field(default_factory=dict)
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True

    @classmethod
    def get_default(cls) -> "ProviderConfig":
        """Get default configuration from environment variables"""
        provider = os.getenv("AI_PROVIDER", "openai")
        model = os.getenv("AI_MODEL", "gpt-3.5-turbo")
        temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("AI_MAX_TOKENS", "1000"))

        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not configured")
        elif provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OpenRouter API key not configured")
        else:
            raise ValueError(f"Unknown AI provider: {provider}")

        return cls(
            provider=provider,
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            provider_options={},
        )


class AIConfig:
    """AI Configuration utilities"""

    @staticmethod
    def get_default() -> ProviderConfig:
        """Get default provider configuration from environment variables"""
        provider = os.getenv("AI_PROVIDER", "openai")
        model = os.getenv("AI_MODEL", "gpt-3.5-turbo")
        temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("AI_MAX_TOKENS", "1000"))

        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not configured")
        elif provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OpenRouter API key not configured")
        else:
            raise ValueError(f"Unknown AI provider: {provider}")

        return ProviderConfig(
            provider=provider,
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
