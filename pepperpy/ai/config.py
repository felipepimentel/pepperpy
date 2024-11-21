"""AI configuration"""

import os
from dataclasses import asdict, dataclass, field
from typing import Any, ClassVar, Optional

from pepperpy.core.db.vector import VectorConfig
from pepperpy.core.types import JsonDict, ModuleConfig


@dataclass
class AIConfig(ModuleConfig):
    """AI configuration"""

    name: str = "ai"
    provider: str = field(default_factory=lambda: os.getenv("AI_PROVIDER", "openrouter"))
    model: str = field(default_factory=lambda: os.getenv("AI_MODEL", "openai/gpt-4-turbo"))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("AI_MAX_TOKENS", "1000")))
    temperature: float = field(default_factory=lambda: float(os.getenv("AI_TEMPERATURE", "0.7")))
    api_key: str = field(default="", repr=False)
    vector_enabled: bool = False
    vector_config: Optional[VectorConfig] = None
    metadata: JsonDict = field(default_factory=dict)
    _instance: ClassVar[Any] = None

    @classmethod
    def get_default(cls) -> "AIConfig":
        """Get default configuration instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            k: v.to_dict() if hasattr(v, "to_dict") else v
            for k, v in asdict(self).items()
            if not k.startswith("_") and k != "api_key"
        }