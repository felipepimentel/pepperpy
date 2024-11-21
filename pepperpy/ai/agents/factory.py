"""Agent factory implementation"""

from typing import TYPE_CHECKING, Any

from pepperpy.ai.config.agent import AgentConfig
from pepperpy.ai.roles import AgentRole

from .analysis import AnalysisAgent, DataAnalystAgent
from .architect import ArchitectAgent
from .base import BaseAgent
from .development import DevelopmentAgent
from .qa import QAAgent
from .review import ReviewAgent

if TYPE_CHECKING:
    from pepperpy.ai.client import AIClient


class AgentFactory:
    """Factory for creating agents"""

    @staticmethod
    def create_agent(
        role: str | AgentRole,
        client: AIClient,
        config: AgentConfig,
        **kwargs: Any,
    ) -> BaseAgent:
        """Create agent instance"""
        if isinstance(role, str):
            role = AgentRole(role)

        agents = {
            AgentRole.ARCHITECT: ArchitectAgent,
            AgentRole.DEVELOPER: DevelopmentAgent,
            AgentRole.REVIEWER: ReviewAgent,
            AgentRole.ANALYST: AnalysisAgent,
            AgentRole.QA: QAAgent,
            AgentRole.RESEARCHER: DataAnalystAgent,
        }

        agent_class = agents.get(role)
        if not agent_class:
            raise ValueError(f"Unknown agent role: {role}")

        return agent_class(client=client, config=config, **kwargs)
