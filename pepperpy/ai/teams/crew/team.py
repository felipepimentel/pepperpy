"""Crew team implementation"""

from typing import Any, Sequence

from pepperpy.ai.client import AIClient
from pepperpy.ai.config.agent import AgentConfig
from pepperpy.ai.types import AIMessage, AIResponse, MessageRole

from ..base import BaseTeam
from ..config import TeamConfig


class CrewTeam(BaseTeam):
    """Crew team implementation"""

    def __init__(
        self, config: TeamConfig, agent_configs: Sequence[AgentConfig], ai_client: AIClient
    ) -> None:
        """Initialize team.

        Args:
            config: Team configuration
            agent_configs: Agent configurations
            ai_client: AI client
        """
        super().__init__(config=config, agent_configs=agent_configs, ai_client=ai_client)
        self.agent_configs = agent_configs
        self._ai_client = ai_client

    async def _initialize(self) -> None:
        """Initialize team"""
        if not self._ai_client.is_initialized:
            await self._ai_client.initialize()

    async def _cleanup(self) -> None:
        """Cleanup team resources"""
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
