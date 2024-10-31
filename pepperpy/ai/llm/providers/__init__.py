"""LLM providers initialization."""
from typing import Optional, Dict, Any
from .base import BaseLLM
from .stackspot import StackspotLLM
from .openrouter import OpenRouterLLM

PROVIDERS = {
    "stackspot": StackspotLLM,
    "openrouter": OpenRouterLLM
}

def get_llm(
    provider: str,
    **kwargs
) -> BaseLLM:
    """Get LLM instance by provider name."""
    if provider not in PROVIDERS:
        raise ValueError(
            f"Unknown provider: {provider}. Available: {list(PROVIDERS.keys())}"
        )
    return PROVIDERS[provider](**kwargs) 