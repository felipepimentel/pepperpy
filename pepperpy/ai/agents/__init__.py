"""AI agents module"""

from .analysis import AnalysisAgent
from .architect import ArchitectAgent
from .base import BaseAgent
from .development import DevelopmentAgent
from .factory import AgentFactory
from .interfaces import (
    AnalystAgent,
    ProjectManagerAgent,
)
from .interfaces import (
    QAAgent as QAAgentProtocol,
)
from .interfaces import (
    ResearchAgent as ResearchAgentProtocol,
)
from .interfaces import (
    ReviewerAgent as ReviewerAgentProtocol,
)
from .qa import QAAgent
from .research import ResearchAgent
from .reviewer import ReviewerAgent
from .team import AgentTeam
from .team_types import TeamConfig, TeamResult, TeamRole
from .types import AgentConfig, AgentRole

__all__ = [
    # Base
    "BaseAgent",
    # Agents
    "AnalysisAgent",
    "ArchitectAgent",
    "DevelopmentAgent",
    "QAAgent",
    "ResearchAgent",
    "ReviewerAgent",
    # Interfaces
    "AnalystAgent",
    "ProjectManagerAgent",
    "QAAgentProtocol",
    "ResearchAgentProtocol",
    "ReviewerAgentProtocol",
    # Team
    "AgentTeam",
    "TeamConfig",
    "TeamResult",
    "TeamRole",
    # Factory
    "AgentFactory",
    # Types
    "AgentConfig",
    "AgentRole",
]
