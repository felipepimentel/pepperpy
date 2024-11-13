"""LLM configuration"""

from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any, Dict, Literal, Optional

ProviderType = Literal["openai", "openrouter", "stackspot"]


@dataclass
class BaseConfig(ABC):
    """Base configuration interface"""

    provider: ProviderType
    api_key: str
    model: str

    def __post_init__(self) -> None:
        """Validate configuration"""
        if not self.api_key:
            raise ValueError("API key is required")
        if not self.provider:
            raise ValueError("Provider is required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return asdict(self)


@dataclass
class OpenAIConfig(BaseConfig):
    """OpenAI specific configuration"""

    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    api_base: Optional[str] = None

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        api_base: Optional[str] = None,
    ) -> None:
        super().__init__(provider="openai", api_key=api_key, model=model)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.api_base = api_base


@dataclass
class OpenRouterConfig(BaseConfig):
    """OpenRouter specific configuration"""

    base_url: str = "https://openrouter.ai/api/v1"
    site_url: Optional[str] = None
    site_name: Optional[str] = None

    def __init__(
        self,
        api_key: str,
        model: str = "anthropic/claude-3-sonnet",
        base_url: str = "https://openrouter.ai/api/v1",
        site_url: Optional[str] = None,
        site_name: Optional[str] = None,
    ) -> None:
        super().__init__(provider="openrouter", api_key=api_key, model=model)
        self.base_url = base_url
        self.site_url = site_url
        self.site_name = site_name


@dataclass
class StackSpotConfig(BaseConfig):
    """StackSpot specific configuration"""

    account_slug: str
    client_id: str
    client_key: str
    qc_slug: str
    base_url: str = "https://genai-code-buddy-api.stackspot.com/v1"
    auth_url: str = "https://idm.stackspot.com"

    def __init__(
        self,
        account_slug: str,
        client_id: str,
        client_key: str,
        qc_slug: str,
        model: str = "stackspot-ai",
        base_url: str = "https://genai-code-buddy-api.stackspot.com/v1",
        auth_url: str = "https://idm.stackspot.com",
    ) -> None:
        super().__init__(provider="stackspot", api_key=client_key, model=model)
        self.account_slug = account_slug
        self.client_id = client_id
        self.client_key = client_key
        self.qc_slug = qc_slug
        self.base_url = base_url
        self.auth_url = auth_url
