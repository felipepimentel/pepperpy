"""AI configuration management."""
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import yaml

@dataclass
class AIConfig:
    """Central configuration for AI functionality."""
    llm_provider: str = "openrouter"
    default_model: str = "anthropic/claude-3-sonnet"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Resource limits
    max_tokens: Optional[int] = None
    max_cost: Optional[float] = None
    
    # RAG settings
    chunk_size: int = 1000
    chunk_overlap: int = 100
    similarity_threshold: float = 0.7
    
    # Cache settings
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    
    # Additional settings
    extra: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_file(cls, path: str) -> "AIConfig":
        """Load configuration from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)
    
    def save(self, path: str) -> None:
        """Save configuration to YAML file."""
        with open(path, 'w') as f:
            yaml.dump(self.__dict__, f) 