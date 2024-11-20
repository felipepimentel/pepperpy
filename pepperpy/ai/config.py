"""AI configuration module"""

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Literal

from pepperpy.core.types import JsonDict
from pepperpy.db.vector import VectorConfig

AIProvider = Literal["openai", "anthropic", "cohere", "openrouter"]
AIModel = Literal[
    "gpt-4",
    "gpt-3.5-turbo",
    "claude-3-opus",
    "claude-3-sonnet",
    "command",
    "command-light",
    "anthropic/claude-3-sonnet",
    "default",
]


class ProviderType(str, Enum):
    """Supported AI providers"""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    OPENROUTER = "openrouter"


@dataclass
class AIConfig:
    """AI configuration"""

    provider: AIProvider = "openrouter"
    model: AIModel = "anthropic/claude-3-sonnet"
    api_key: str | None = None
    api_base: str | None = None
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: list[str] | None = None
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    vector_enabled: bool = False
    vector_config: VectorConfig | None = None
    metadata: JsonDict = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict)  # Provider-specific parameters

    def __post_init__(self) -> None:
        """Validate configuration"""
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("Temperature must be between 0 and 1")

        if self.max_tokens < 1:
            raise ValueError("Max tokens must be positive")

        if self.top_p < 0 or self.top_p > 1:
            raise ValueError("Top P must be between 0 and 1")

        if self.frequency_penalty < -2 or self.frequency_penalty > 2:
            raise ValueError("Frequency penalty must be between -2 and 2")

        if self.presence_penalty < -2 or self.presence_penalty > 2:
            raise ValueError("Presence penalty must be between -2 and 2")

        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")

        if self.retry_attempts < 0:
            raise ValueError("Retry attempts must be non-negative")

        if self.retry_delay < 0:
            raise ValueError("Retry delay must be non-negative")

        if self.cache_ttl < 0:
            raise ValueError("Cache TTL must be non-negative")

        if self.provider not in [e.value for e in ProviderType]:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self) 