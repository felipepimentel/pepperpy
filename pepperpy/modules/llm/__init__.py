"""LLM module initialization."""
from .base import BaseLLM
from .providers import StackspotLLM, OpenRouterLLM
from .tools import Tool, ToolManager
from .types import Message, ModelInfo, Conversation

def get_llm(provider: str, **kwargs) -> BaseLLM:
    """Get LLM instance by provider name."""
    providers = {
        "stackspot": StackspotLLM,
        "openrouter": OpenRouterLLM
    }
    
    if provider not in providers:
        raise ValueError(f"Unknown provider: {provider}")
        
    return providers[provider](**kwargs) 