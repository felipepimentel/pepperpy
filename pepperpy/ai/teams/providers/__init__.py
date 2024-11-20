"""Team providers module"""

from typing import Any

from pepperpy.ai.client import AIClient

from ..types import TeamConfig, TeamFramework
from .autogen import AutoGenProvider
from .base import TeamProvider
from .crew import CrewProvider
from .langchain import LangChainProvider

__all__ = [
    "get_provider",
    "TeamProvider",
    "AutoGenProvider",
    "CrewProvider", 
    "LangChainProvider"
]


async def get_provider(
    framework: TeamFramework,
    config: TeamConfig,
    ai_client: AIClient | None = None,
    **kwargs: Any,
) -> TeamProvider:
    """Get team provider based on framework"""
    providers = {
        TeamFramework.AUTOGEN: AutoGenProvider,
        TeamFramework.CREW: CrewProvider,
        TeamFramework.LANGCHAIN: LangChainProvider
    }

    provider_class = providers.get(framework)
    if not provider_class:
        raise ValueError(f"Unsupported framework: {framework}")

    return provider_class(config, ai_client, **kwargs) 