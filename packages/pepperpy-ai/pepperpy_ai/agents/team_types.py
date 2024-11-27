"""Team type definitions"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from bko.ai.roles import AgentRole
from bko.ai.types import AIResponse


@dataclass
class TeamRole:
    """Team role definition"""

    name: str
    description: str
    responsibilities: List[str]


@dataclass
class TeamMember:
    """Team member definition"""

    name: str
    role: TeamRole
    agent_role: AgentRole
    expertise: List[str]


@dataclass
class TeamConfig:
    """Team configuration"""

    name: str
    description: str
    roles: List[TeamRole]
    members: List[TeamMember]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration"""
        if not self.name:
            raise ValueError("Team name cannot be empty")


@dataclass
class TeamContext:
    """Team context information"""

    task_id: str
    team_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TeamTask:
    """Team task definition"""

    id: str
    description: str
    assignee: str
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate task"""
        if not self.id:
            raise ValueError("Task ID cannot be empty")


@dataclass
class TeamResult:
    """Team task result"""

    task_id: str
    status: str
    success: bool = field(default=False)
    output: Optional[AIResponse] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[Dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate result"""
        if not self.task_id:
            raise ValueError("Task ID cannot be empty")
        if not self.status:
            raise ValueError("Status cannot be empty")
        if self.status == "completed" and not self.success:
            self.success = True
        elif self.status == "failed" and self.success:
            self.success = False
