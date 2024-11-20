"""Agent type definitions"""

from dataclasses import dataclass, field
from enum import Enum

from pepperpy.core.types import JsonDict


class AgentRole(str, Enum):
    """Agent roles"""

    ARCHITECT = "architect"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    ANALYST = "analyst"
    QA = "qa"
    RESEARCHER = "researcher"
    MANAGER = "manager"
    INTEGRATION = "integration"


@dataclass
class AgentConfig:
    """Agent configuration"""

    name: str
    role: AgentRole
    enabled: bool = True
    max_retries: int = 3
    timeout: float = 60.0
    metadata: JsonDict = field(default_factory=dict)
