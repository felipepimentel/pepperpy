"""Team type definitions"""

from dataclasses import dataclass, field
from enum import Enum

from pepperpy.core.types import JsonDict


class TeamRole(str, Enum):
    """Team member roles"""

    ARCHITECT = "architect"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    ANALYST = "analyst"
    QA = "qa"
    DEVOPS = "devops"
    SECURITY = "security"
    MANAGER = "manager"


@dataclass
class TeamConfig:
    """Team configuration"""

    name: str
    roles: list[TeamRole] = field(default_factory=list)
    enabled: bool = True
    parallel: bool = False
    max_rounds: int = 10
    timeout: float = 300.0  # 5 minutes
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TeamResult:
    """Team execution result"""

    success: bool
    output: str | None = None
    metadata: JsonDict = field(default_factory=dict)
