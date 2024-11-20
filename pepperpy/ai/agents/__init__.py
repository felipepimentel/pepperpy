"""AI agents module"""

from .analysis import AnalysisAgent, DataAnalystAgent, IntegrationAgent
from .base import BaseAgent
from .factory import AgentFactory
from .interfaces import (
    AnalystAgent,
    ArchitectAgent,
    DeveloperAgent,
    ProjectManagerAgent,
    QAAgent,
    ReviewerAgent,
)
from .research import ResearchAgent
from .types import AgentConfig, AgentRole, AgentType

__all__ = [
    # Base
    "BaseAgent",
    "AgentConfig",
    "AgentFactory",
    # Agents
    "AnalysisAgent",
    "AnalystAgent",
    "ArchitectAgent",
    "DataAnalystAgent",
    "DeveloperAgent",
    "IntegrationAgent",
    "ProjectManagerAgent",
    "QAAgent",
    "ResearchAgent",
    "ReviewerAgent",
    # Types
    "AgentRole",
    "AgentType",
]
