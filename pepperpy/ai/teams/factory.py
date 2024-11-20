"""Team factory implementation"""

from typing import Any, cast

from pepperpy.ai.client import AIClient

from .interfaces import BaseTeam
from .providers import get_provider
from .types import TeamConfig


class TeamFactory:
    """Factory for creating teams"""

    @staticmethod
    async def create_team(
        config: TeamConfig,
        ai_client: AIClient | None = None,
        **kwargs: Any,
    ) -> BaseTeam:
        """Create team instance based on configuration"""
        provider = await get_provider(config.framework, config, ai_client, **kwargs)
        return cast(BaseTeam, provider) 