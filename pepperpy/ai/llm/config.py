"""LLM configuration"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from pepperpy.core.config import ModuleConfig


@dataclass
class LLMConfig(ModuleConfig):
    """Configuration for LLM operations"""

    provider: str = "openai"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    api_key: Optional[str] = None
    api_base: Optional[str] = None

    def dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self)
