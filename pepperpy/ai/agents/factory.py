"""Agent factory implementation"""

from typing import Any

from ..client import AIClient
from ..exceptions import AIError
from .analysis import AnalysisAgent
from .architect import ArchitectAgent
from .base import BaseAgent
from .development import DevelopmentAgent
from .management import ProjectManagerAgent
from .qa import QAAgent
from .researcher import ResearcherAgent
from .specialized import (
    CodeReviewAgent,
    DocumentationAgent,
    OptimizationAgent,
    SecurityAgent,
    TestingAgent,
)
from .types import AgentConfig


class AgentFactory:
    """Factory for creating agents"""

    _agent_types = {
        "researcher": ResearcherAgent,
        "analyst": AnalysisAgent,
        "architect": ArchitectAgent,
        "project_manager": ProjectManagerAgent,
        "developer": DevelopmentAgent,
        "qa": QAAgent,
        "reviewer": CodeReviewAgent,
        "tester": TestingAgent,
        "optimizer": OptimizationAgent,
        "security": SecurityAgent,
        "documentation": DocumentationAgent,
    }

    @classmethod
    def create_agent(
        cls,
        agent_type: str,
        client: AIClient,
        config: AgentConfig | None = None,
        **kwargs: Any,
    ) -> BaseAgent:
        """Create agent instance"""
        try:
            if agent_type not in cls._agent_types:
                raise AIError(f"Unknown agent type: {agent_type}")

            agent_class = cls._agent_types[agent_type]
            return agent_class(client=client, **kwargs)

        except Exception as e:
            raise AIError(f"Failed to create agent: {e}", cause=e) 