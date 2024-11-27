"""Team manager implementation"""

from typing import Sequence

from bko.ai.config.agent import AgentConfig
from bko.core.module import InitializableModule
from bko.core.validation import ValidatorFactory

from ..client import AIClient
from .autogen.team import AutogenTeam
from .base import BaseTeam
from .config import TeamConfig, TeamFramework
from .crew.team import CrewTeam
from .langchain.team import LangchainTeam


class TeamManager(InitializableModule):
    """Team manager implementation"""

    def __init__(self) -> None:
        super().__init__()
        self._config_validator = ValidatorFactory.create_schema_validator(TeamConfig)
        self._teams: dict[str, BaseTeam] = {}

    async def _initialize(self) -> None:
        """Initialize team manager"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup team manager"""
        for team in self._teams.values():
            await team.cleanup()
        self._teams.clear()

    async def create_team(
        self,
        config: TeamConfig,
        agent_configs: Sequence[AgentConfig],
        ai_client: AIClient,
    ) -> BaseTeam:
        """Create new team"""
        self._ensure_initialized()

        result = await self._config_validator.validate(config.model_dump())
        if not result.is_valid:
            raise ValueError(f"Invalid team configuration: {', '.join(result.errors)}")

        team_class = self._get_team_class(config.framework)
        team = team_class(config=config, agent_configs=agent_configs, ai_client=ai_client)
        await team.initialize()

        self._teams[config.name] = team
        return team

    def _get_team_class(self, framework: TeamFramework) -> type[BaseTeam]:
        """Get team class for framework"""
        teams = {
            TeamFramework.AUTOGEN: AutogenTeam,
            TeamFramework.CREW: CrewTeam,
            TeamFramework.LANGCHAIN: LangchainTeam,
        }
        return teams[framework]
