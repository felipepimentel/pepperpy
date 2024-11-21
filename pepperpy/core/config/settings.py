"""Core settings management"""

import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from ..db.vector import VectorConfig
from ..types import JsonDict


class Environment(str, Enum):
    """Application environment"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class CoreSettings:
    """Core application settings"""

    debug: bool = False
    env: Environment = Environment.DEVELOPMENT
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class AISettings:
    """AI module settings"""

    provider: str = "openrouter"
    model: Optional[str] = None
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    vector_enabled: bool = False
    vector_config: Optional[VectorConfig] = None
    metadata: JsonDict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Post initialization"""
        if self.vector_enabled and not self.vector_config:
            self.vector_config = VectorConfig(
                dimension=1536,  # Padrão para embeddings OpenAI
                db_config=None,  # Será configurado quando necessário
            )


@dataclass
class AnalysisSettings:
    """Analysis module settings"""

    output_dir: Path = Path("epub_analysis")
    chunk_size: int = 2000
    chunk_overlap: int = 100
    metadata: JsonDict = field(default_factory=dict)


class Settings:
    """Global settings manager"""

    def __init__(self) -> None:
        """Initialize settings"""
        # Load environment variables
        load_dotenv()

        # Core settings
        self.core = CoreSettings(
            debug=self._get_bool("PEPPERPY_DEBUG", False),
            env=Environment(self._get_str("PEPPERPY_ENV", "development")),
        )

        # AI settings
        self.ai = AISettings(
            provider=self._get_str("AI_PROVIDER"),
            model=self._get_str("AI_MODEL"),
            api_key=self._get_str("OPENROUTER_API_KEY"),
            temperature=self._get_float("AI_TEMPERATURE", 0.7),
            max_tokens=self._get_int("AI_MAX_TOKENS", 1000),
            vector_enabled=self._get_bool("AI_VECTOR_ENABLED", False),
        )

        # Analysis settings
        self.analysis = AnalysisSettings(
            output_dir=Path(self._get_str("ANALYSIS_OUTPUT_DIR", "epub_analysis")),
            chunk_size=self._get_int("ANALYSIS_CHUNK_SIZE", 2000),
            chunk_overlap=self._get_int("ANALYSIS_CHUNK_OVERLAP", 100),
        )

    def _get_str(self, key: str, default: str = "") -> str:
        """Get string value from environment"""
        return os.getenv(key, default)

    def _get_int(self, key: str, default: int) -> int:
        """Get integer value from environment"""
        value = os.getenv(key)
        return int(value) if value is not None else default

    def _get_float(self, key: str, default: float) -> float:
        """Get float value from environment"""
        value = os.getenv(key)
        return float(value) if value is not None else default

    def _get_bool(self, key: str, default: bool) -> bool:
        """Get boolean value from environment"""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes")


# Global settings instance
settings = Settings()
