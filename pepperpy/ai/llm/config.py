"""LLM configuration"""

from dataclasses import dataclass, field
from enum import Enum

from pepperpy.core.types import JsonDict


class LLMProvider(str, Enum):
    """LLM provider types"""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    OPENROUTER = "openrouter"
    STACKSPOT = "stackspot"


@dataclass
class BaseLLMConfig:
    """Base LLM configuration"""

    name: str
    api_key: str
    enabled: bool = True
    api_base: str | None = None
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class OpenAIConfig(BaseLLMConfig):
    """OpenAI provider configuration"""

    organization: str | None = None
    model: str = "gpt-4"


@dataclass
class OpenRouterConfig(BaseLLMConfig):
    """OpenRouter provider configuration"""

    model: str | None = None
    route_prefix: str | None = None


@dataclass
class StackSpotConfig(BaseLLMConfig):
    """StackSpot provider configuration"""

    model: str = "stackspot/stackspot-ai"
    workspace: str | None = None


@dataclass
class LLMConfig:
    """LLM configuration"""

    name: str
    model: str
    provider: LLMProvider
    enabled: bool = True
    api_key: str | None = None
    api_base: str | None = None
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: list[str] = field(default_factory=list)
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    metadata: JsonDict = field(default_factory=dict)
