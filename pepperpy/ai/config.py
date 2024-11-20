"""AI configuration"""

from dataclasses import asdict, dataclass, field
from typing import Any, ClassVar

from pepperpy.core.config.manager import config_manager
from pepperpy.core.types import JsonDict
from pepperpy.db.vector import VectorConfig


@dataclass
class AIConfig:
    """AI configuration"""

    _instance: ClassVar[Any] = None

    provider: str = field(default_factory=lambda: config_manager.settings.ai.provider)
    model: str = field(default_factory=lambda: config_manager.settings.ai.model)
    api_key: str | None = field(default_factory=lambda: config_manager.settings.ai.api_key)
    api_base: str | None = field(default_factory=lambda: config_manager.settings.ai.api_base)
    temperature: float = field(default_factory=lambda: config_manager.settings.ai.temperature)
    max_tokens: int = field(default_factory=lambda: config_manager.settings.ai.max_tokens)
    vector_enabled: bool = field(default_factory=lambda: config_manager.settings.ai.vector_enabled)
    vector_config: VectorConfig | None = field(default_factory=lambda: config_manager.settings.ai.vector_config)
    metadata: JsonDict = field(default_factory=dict)

    @classmethod
    def get_default(cls) -> "AIConfig":
        """Get default configuration instance"""
        if cls._instance is None:
            cls._instance = config_manager.get_config(cls)
        return cls._instance

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        config_dict = asdict(self)
        if self.vector_config:
            config_dict["vector_config"] = asdict(self.vector_config)
        return config_dict 