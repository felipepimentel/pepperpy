from typing import Optional, Type
from .base import BaseLLM
from .stackspot import StackspotLLM
from .openrouter import OpenRouterLLM
from ..core.config import Config

# Mapeamento de providers para implementações
PROVIDERS = {
    "stackspot": StackspotLLM,
    "openrouter": OpenRouterLLM
}

def get_llm(provider: Optional[str] = None, config: Optional[Config] = None) -> BaseLLM:
    """
    Obtém uma instância de LLM configurada.
    
    Args:
        provider: Nome do provider ('stackspot' ou 'openrouter')
        config: Configurações opcionais
        
    Returns:
        BaseLLM: Instância configurada do LLM
    """
    config = config or Config()
    provider = provider or config.get("LLM_PROVIDER", "openrouter")
    
    if provider not in PROVIDERS:
        raise ValueError(f"Provider '{provider}' não suportado. Use: {list(PROVIDERS.keys())}")
        
    return PROVIDERS[provider](config=config) 