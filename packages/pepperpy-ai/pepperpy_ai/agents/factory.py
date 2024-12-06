"""Agent factory implementation."""


from .analysis import AnalysisAgent
from .architect import ArchitectAgent
from .base import BaseAgent
from .development import DevelopmentAgent
from .management import ProjectManagerAgent, QualityEngineerAgent
from .types import AgentConfig, AgentRole

AGENT_TYPES: dict[AgentRole, type[BaseAgent]] = {
    AgentRole.ARCHITECT: ArchitectAgent,
    AgentRole.DEVELOPER: DevelopmentAgent,
    AgentRole.RESEARCHER: AnalysisAgent,
    AgentRole.PLANNER: ProjectManagerAgent,
    AgentRole.REVIEWER: QualityEngineerAgent,
}


def create_agent(config: AgentConfig) -> BaseAgent:
    """Create agent instance.

    Args:
        config: Agent configuration

    Returns:
        Agent instance

    Raises:
        ValueError: If agent type is unknown
    """
    agent_class = AGENT_TYPES.get(config.role)
    if not agent_class:
        raise ValueError(f"Unknown agent role: {config.role}")

    return agent_class(config)
