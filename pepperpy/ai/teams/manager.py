"""Team manager implementation"""

from typing import Any

from pepperpy.core.module import BaseModule

from .factory import TeamFactory
from .interfaces import BaseTeam
from .types import TeamConfig, TeamFramework


class TeamManager(BaseModule):
    """Manages AI teams"""

    def __init__(self) -> None:
        self._teams: dict[str, BaseTeam] = {}

    async def create_team(
        self,
        framework: TeamFramework,
        name: str,
        **kwargs: Any,
    ) -> BaseTeam:
        """Create new team"""
        config = TeamConfig(
            framework=framework,
            name=name,
            **kwargs
        )
        team = await TeamFactory.create_team(config)
        self._teams[name] = team
        return team

    async def get_team(self, name: str) -> BaseTeam:
        """Get existing team"""
        if name not in self._teams:
            raise ValueError(f"Team {name} not found")
        return self._teams[name]

    async def delete_team(self, name: str) -> None:
        """Delete team"""
        if name in self._teams:
            await self._teams[name].cleanup()
            del self._teams[name]

    async def cleanup(self) -> None:
        """Cleanup all teams"""
        for team in self._teams.values():
            await team.cleanup()
        self._teams.clear() 