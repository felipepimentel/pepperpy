"""Team agent implementation"""

from typing import Any, Sequence, Tuple

from pepperpy.core.module import BaseModule

from ..client import AIClient
from .base import BaseAgent
from .team_types import TeamConfig, TeamResult


class AgentTeam(BaseModule[TeamConfig]):
    """Team of agents working together"""

    def __init__(self, config: TeamConfig, ai_client: AIClient) -> None:
        super().__init__(config)
        self._client = ai_client
        self._agents: dict[str, BaseAgent] = {}

    async def _initialize(self) -> None:
        """Initialize team"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        for agent in self._agents.values():
            await agent.cleanup()

    def add_agent(self, name: str, agent: BaseAgent) -> None:
        """Add agent to team"""
        self._agents[name] = agent

    async def coordinate(
        self, tasks: Sequence[Tuple[BaseAgent, str]], **kwargs: Any
    ) -> TeamResult:
        """Coordinate team tasks"""
        if not self._initialized:
            await self.initialize()

        results = []
        for agent, task in tasks:
            result = await agent.execute(task, **kwargs)
            results.append(result)

        return TeamResult(
            success=all(r.success for r in results),
            output="\n\n".join(r.content for r in results),
            metadata={"results": results}
        )
