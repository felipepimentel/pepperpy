"""Team type definitions"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol, Sequence, Tuple

from ..exceptions import AIError
from ..types import AIConfig, AIResponse


class BaseAgent(Protocol):
    """Base agent protocol"""

    async def execute(self, task: str) -> AIResponse:
        """Execute agent task"""
        ...


class TeamRole(Enum):
    """Team role enumeration"""

    ARCHITECT = auto()
    DEVELOPER = auto()
    REVIEWER = auto()
    TESTER = auto()
    QA = auto()
    DEVOPS = auto()
    SECURITY = auto()


@dataclass
class TeamConfig:
    """Team configuration"""

    name: str
    roles: list[TeamRole]
    ai_config: AIConfig
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentTeam:
    """Agent team implementation"""

    config: TeamConfig
    agents: dict[str, BaseAgent] = field(default_factory=dict)

    async def coordinate(self, tasks: Sequence[Tuple[BaseAgent, str]]) -> list[AIResponse]:
        """Coordinate team tasks"""
        try:
            results = []
            for agent, task in tasks:
                if hasattr(agent, "execute"):
                    result = await agent.execute(task)
                    results.append(result)
                else:
                    raise AIError(f"Agent {agent.__class__.__name__} missing execute method")
            return results
        except Exception as e:
            raise AIError(f"Team coordination failed: {e}", cause=e)
