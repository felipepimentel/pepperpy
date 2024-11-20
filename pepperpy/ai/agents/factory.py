"""Agent factory implementation"""

from typing import Any

from pepperpy.core.module import BaseModule

from ..client import AIClient
from .analysis import AnalysisAgent, DataAnalystAgent
from .base import BaseAgent
from .research import ResearchAgent as ResearchAgentImpl
from .types import AgentConfig, AgentType


class AgentFactory(BaseModule):
    """Factory for creating agents"""

    @staticmethod
    def create_agent(
        agent_type: str,
        client: AIClient,
        config: AgentConfig,
        **kwargs: Any,
    ) -> BaseAgent:
        """Create agent instance"""
        agents = {
            AgentType.ANALYSIS.value: AnalysisAgent,
            AgentType.RESEARCH.value: ResearchAgentImpl,
            "data_analyst": DataAnalystAgent,
            "researcher": ResearchAgentImpl,  # Alias para research
        }

        agent_class = agents.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")

        return agent_class(client=client, config=config, **kwargs) 