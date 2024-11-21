"""Team type definitions"""

from dataclasses import field
from enum import Enum

from pydantic import BaseModel

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


class TeamConfig(BaseModel):
    """Team configuration"""

    name: str
    roles: list[TeamRole] = field(default_factory=list)
    enabled: bool = True
    parallel: bool = False
    max_rounds: int = 10
    timeout: float = 300.0  # 5 minutes
    metadata: JsonDict = field(default_factory=dict)


class TeamResult(BaseModel):
    """Team execution result"""

    success: bool
    output: str | None = None
    metadata: JsonDict = field(default_factory=dict)
