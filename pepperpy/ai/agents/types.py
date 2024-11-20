"""Agent type definitions"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from pepperpy.core.types import JsonDict

from ..config import AIConfig


class AgentRole(str, Enum):
    """Agent roles"""

    ANALYST = "analyst"
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    MANAGER = "manager"
    QA = "qa"
    RESEARCHER = "researcher"
    REVIEWER = "reviewer"


class AgentType(str, Enum):
    """Agent types"""

    ANALYSIS = "analysis"
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    INTEGRATION = "integration"
    MANAGER = "manager"
    QA = "qa"
    RESEARCH = "research"
    REVIEWER = "reviewer"


@dataclass
class AgentConfig:
    """Agent configuration"""

    name: str
    role: str
    ai_config: AIConfig
    metadata: JsonDict = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict) 