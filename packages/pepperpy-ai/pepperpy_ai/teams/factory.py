"""Team factory implementation"""

from typing import Sequence

from bko.ai.config.agent import AgentConfig

from ..client import AIClient
from .autogen.team import AutogenTeam
from .base import BaseTeam
from .config import TeamConfig, TeamFramework
from .crew.team import CrewTeam
from .langchain.team import LangchainTeam


class TeamFactory:
    """Factory for creating AI teams"""

    _teams = {
        TeamFramework.AUTOGEN: AutogenTeam,
        TeamFramework.CREW: CrewTeam,
        TeamFramework.LANGCHAIN: LangchainTeam,
    }

    @classmethod
    async def create_team(
        cls,
        config: TeamConfig,
        agent_configs: Sequence[AgentConfig],
        ai_client: AIClient,
    ) -> BaseTeam:
        """Create team instance"""
        team_class = cls._teams.get(config.framework)
        if not team_class:
            raise ValueError(f"Unknown team framework: {config.framework}")

        team = team_class(config, agent_configs, ai_client)
        await team.initialize()
        return team

    @classmethod
    def get_team_class(cls, framework: TeamFramework) -> type[BaseTeam]:
        """Get team class for framework"""
        team_class = cls._teams.get(framework)
        if not team_class:
            raise ValueError(f"Unknown team framework: {framework}")
        return team_class
