"""Agent type definitions."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

JsonDict = dict[str, Any]


class AgentRole(str, Enum):
    """Agent role types."""

    ARCHITECT = "architect"
    DEVELOPER = "developer"
    REVIEWER = "reviewer"
    RESEARCHER = "researcher"
    PLANNER = "planner"
    EXECUTOR = "executor"
    ASSISTANT = "assistant"


@dataclass
class AgentConfig:
    """Agent configuration."""

    name: str
    role: AgentRole
    metadata: JsonDict = field(default_factory=dict)
