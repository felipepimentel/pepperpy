"""Crew team implementation"""

from typing import Any

from ...types import AIMessage, AIResponse, MessageRole
from ..base import BaseTeam


class CrewTeam(BaseTeam):
    """Crew team implementation"""

    async def _initialize(self) -> None:
        """Initialize team"""
        if not self._ai_client.is_initialized:
            await self._ai_client.initialize()

    async def _cleanup(self) -> None:
        """Cleanup team resources"""
        for agent in self.agent_configs:
            await self._ai_client.complete(
                f"Finalizing {agent.name}'s tasks and saving context"
            )

    async def execute_task(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute team task"""
        self._ensure_initialized()
        
        messages = [AIMessage(role=MessageRole.USER, content=task)]
        
        # Distribuir tarefa entre os agentes
        for agent in self.agent_configs:
            agent_prompt = (
                f"As {agent.name} with role {agent.role}, "
                f"analyze and contribute to: {task}"
            )
            agent_response = await self._ai_client.complete(agent_prompt)
            messages.append(
                AIMessage(
                    role=MessageRole.ASSISTANT,
                    content=agent_response.content,
                    metadata={"agent": agent.name, "role": agent.role}
                )
            )

        # Consolidar resultados
        consolidation_prompt = (
            "Review and consolidate all agent contributions into a final response:\n" +
            "\n".join(f"- {m.content}" for m in messages if m.role == MessageRole.ASSISTANT)
        )
        
        final_response = await self._ai_client.complete(consolidation_prompt)
        messages.append(
            AIMessage(
                role=MessageRole.ASSISTANT,
                content=final_response.content,
                metadata={"phase": "consolidation"}
            )
        )

        return AIResponse(
            content=final_response.content,
            messages=messages,
            metadata={
                "team": "crew",
                "agents": [a.name for a in self.agent_configs],
                "task": task
            }
        )
