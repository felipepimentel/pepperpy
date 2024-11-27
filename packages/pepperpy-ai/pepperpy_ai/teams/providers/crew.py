"""Crew team provider implementation"""

from typing import Any, Sequence

from bko.ai.client import AIClient
from bko.ai.config.agent import AgentConfig
from bko.ai.teams.base import BaseTeam
from bko.ai.teams.config import TeamConfig
from bko.ai.types import AIMessage, AIResponse, MessageRole


class CrewTeamProvider(BaseTeam):
    """Crew team provider implementation"""

    def __init__(
        self, config: TeamConfig, agent_configs: Sequence[AgentConfig], ai_client: AIClient
    ) -> None:
        """Initialize provider"""
        super().__init__(config=config, agent_configs=agent_configs, ai_client=ai_client)
        self.agent_configs = agent_configs
        self._ai_client = ai_client

    async def _setup(self) -> None:
        """Setup provider resources"""
        if not self._ai_client.is_initialized:
            await self._ai_client.initialize()

    async def _teardown(self) -> None:
        """Teardown provider resources"""
        for agent in self.agent_configs:
            await self._ai_client.complete(f"Finalizing {agent.name}'s tasks and saving context")

    async def execute_task(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute team task"""
        self._ensure_initialized()

        messages = [AIMessage(role=MessageRole.USER, content=task)]

        for agent in self.agent_configs:
            agent_prompt = (
                f"As {agent.name} with role {agent.role}, " f"analyze and contribute to: {task}"
            )
            agent_response = await self._ai_client.complete(agent_prompt)
            messages.append(AIMessage(role=MessageRole.ASSISTANT, content=agent_response.content))

        consolidation_prompt = (
            "Review and consolidate all agent contributions into a final response:\n"
            + "\n".join(f"- {m.content}" for m in messages if m.role == MessageRole.ASSISTANT)
        )

        final_response = await self._ai_client.complete(consolidation_prompt)
        messages.append(AIMessage(role=MessageRole.ASSISTANT, content=final_response.content))

        return AIResponse(
            content=final_response.content,
            messages=messages,
            metadata={
                "provider": "crew",
                "agents": [a.name for a in self.agent_configs],
                "task": task,
                **kwargs,
            },
        )

    async def get_team_members(self) -> Sequence[str]:
        """Get team member names"""
        self._ensure_initialized()
        return [agent.name for agent in self.agent_configs]

    async def get_team_roles(self) -> dict[str, str]:
        """Get team member roles"""
        self._ensure_initialized()
        return {agent.name: agent.role for agent in self.agent_configs}
