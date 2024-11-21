"""Provider type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pepperpy.core.types import JsonDict


@dataclass
class ProviderResponse:
    """Provider response"""

    content: str
    model: str
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class OpenRouterConfig:
    """OpenRouter provider configuration"""

    name: str
    api_key: str
    model: str | None = None
    enabled: bool = True
    api_base: str = "https://openrouter.ai/api/v1"
    site_url: str | None = None
    site_name: str | None = None
    route_prefix: str | None = None
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    metadata: JsonDict = field(default_factory=dict)
