"""LLM configuration"""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class BaseConfig:
    """Base configuration for LLM providers"""

    api_key: str
    model: str
    provider: str

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self)


@dataclass
class OpenAIConfig(BaseConfig):
    """OpenAI configuration"""

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> None:
        super().__init__(
            api_key=api_key,
            model=model,
            provider="openai",
        )
        self.temperature = temperature
        self.max_tokens = max_tokens


@dataclass
class OpenRouterConfig(BaseConfig):
    """OpenRouter configuration"""

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.7,
        generation_config: dict[str, Any] | None = None,
        site_url: str | None = None,
        site_name: str | None = None,
        timeout: int = 30,
    ) -> None:
        super().__init__(
            api_key=api_key,
            model=model,
            provider="openrouter",
        )
        self.temperature = temperature
        self.generation_config = generation_config or {}
        self.site_url = site_url
        self.site_name = site_name
        self.timeout = timeout


@dataclass
class StackSpotConfig(BaseConfig):
    """StackSpot configuration"""

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        base_url: str = "https://api.stackspot.com",
        auth_url: str = "https://auth.stackspot.com",
        account_slug: str = "default",
        client_id: str = "",
        client_key: str = "",
    ) -> None:
        super().__init__(
            api_key=api_key,
            model=model,
            provider="stackspot",
        )
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = base_url
        self.auth_url = auth_url
        self.account_slug = account_slug
        self.client_id = client_id
        self.client_key = client_key
