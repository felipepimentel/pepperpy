"""Agent type definitions"""

from dataclasses import dataclass, field
from typing import Any

from ..types import AIConfig


@dataclass
class AgentConfig:
    """Base agent configuration"""

    name: str
    role: str
    ai_config: AIConfig
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AssistantAgent:
    """Assistant agent configuration"""

    config: AgentConfig
    personality: str = "helpful"
    expertise: list[str] = field(default_factory=list)


@dataclass
class ExpertAgent:
    """Expert agent configuration"""

    config: AgentConfig
    domain: str
    skills: list[str] = field(default_factory=list)


@dataclass
class TeamAgent:
    """Team agent configuration"""

    config: AgentConfig
    members: list[str] = field(default_factory=list)
    roles: dict[str, str] = field(default_factory=dict) 