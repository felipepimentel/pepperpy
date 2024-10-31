"""AI capabilities for Pepperpy."""
from typing import Optional, Dict, Any
from pathlib import Path

from .core.config import AIConfig
from .llm import get_llm
from .pipelines.rag import RAGPipeline
from .pipelines.agents import AgentSystem

class AI:
    """Main entry point for AI functionality."""
    
    def __init__(
        self,
        config: Optional[AIConfig] = None,
        config_path: Optional[str] = None
    ):
        """Initialize AI with configuration."""
        if config_path:
            self.config = AIConfig.from_file(config_path)
        else:
            self.config = config or AIConfig()
            
        # Initialize components
        self.llm = get_llm(
            provider=self.config.llm_provider,
            model=self.config.default_model
        )
        
        # Initialize pipelines
        self.rag = RAGPipeline(
            llm=self.llm,
            config=self.config
        )
        
        self.agents = AgentSystem(
            llm=self.llm,
            config=self.config
        )
    
    @classmethod
    def from_config(cls, config_path: str) -> "AI":
        """Create AI instance from config file."""
        return cls(config_path=config_path)
    
    def save_config(self, path: str) -> None:
        """Save current configuration."""
        self.config.save(path)

# Convenience functions
def setup(config: Optional[Dict[str, Any]] = None) -> AI:
    """Setup and return AI instance."""
    return AI(AIConfig(**(config or {})))

__all__ = ['AI', 'setup', 'get_llm', 'RAGPipeline', 'AgentSystem'] 