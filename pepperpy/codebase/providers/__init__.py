"""Code analysis providers"""

from typing import Any

from pepperpy.ai.client import AIClient

from ..config import CodebaseConfig, ProviderType
from .base import BaseCodeProvider
from .hybrid import HybridProvider
from .static import StaticAnalysisProvider

__all__ = [
    "get_provider",
    "BaseCodeProvider",
    "HybridProvider",
    "StaticAnalysisProvider",
]


async def get_provider(
    provider_type: ProviderType,
    config: CodebaseConfig,
    ai_client: AIClient | None = None,
    **kwargs: Any,
) -> BaseCodeProvider:
    """Get code analysis provider"""
    providers = {
        ProviderType.STATIC: StaticAnalysisProvider,
        ProviderType.HYBRID: HybridProvider,
    }

    provider_class = providers.get(provider_type)
    if not provider_class:
        raise ValueError(f"Unsupported provider type: {provider_type}")

    if provider_type == ProviderType.HYBRID and not ai_client:
        raise ValueError("AI client required for hybrid provider")

    if provider_type == ProviderType.HYBRID:
        return provider_class(ai_client)
    return provider_class() 