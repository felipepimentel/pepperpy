"""Agent factory implementation"""

from typing import Any

from ..client import AIClient
from .analysis import AnalysisAgent
from .architect import ArchitectAgent
from .base import BaseAgent
from .development import DevelopmentAgent
from .qa import QAAgent
from .research import ResearchAgent
from .reviewer import ReviewerAgent
from .types import AgentConfig, AgentRole


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
            AgentRole.REVIEWER: ReviewerAgent,
            AgentRole.ANALYST: AnalysisAgent,
            AgentRole.QA: QAAgent,
            AgentRole.RESEARCHER: ResearchAgent,
        }

        agent_class = agents.get(role)
        if not agent_class:
            raise ValueError(f"Unknown agent role: {role}")

        return agent_class(client=client, config=config, **kwargs) 