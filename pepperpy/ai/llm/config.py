"""LLM configuration"""

from dataclasses import dataclass
from typing import Dict, Optional

from pepperpy.core.config import ModuleConfig


@dataclass
class LLMConfig(ModuleConfig):
    """Configuration for language models"""

    provider: str = "openai"  # openai, anthropic, local, etc.
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: Optional[list[str]] = None
    timeout: float = 30.0
    retry_count: int = 3
    retry_delay: float = 1.0
    streaming: bool = False
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    api_version: Optional[str] = None
    organization_id: Optional[str] = None
    extra_headers: Dict[str, str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.extra_headers is None:
            self.extra_headers = {}
