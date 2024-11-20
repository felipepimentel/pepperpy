"""Team interfaces and protocols"""

from abc import ABC, abstractmethod
from typing import Any, Protocol

from .types import TeamResult


class TeamAgent(Protocol):
    """Base agent interface"""

    async def initialize(self) -> None:
        """Initialize agent"""
        ...

    async def execute(self, task: str, **kwargs: Any) -> Any:
        """Execute task"""
        ...

    async def cleanup(self) -> None:
        """Cleanup agent resources"""
        ...


class TeamTool(Protocol):
    """Base tool interface"""

    async def initialize(self) -> None:
        """Initialize tool"""
        ...

    async def execute(self, **kwargs: Any) -> Any:
        """Execute tool"""
        ...

    async def cleanup(self) -> None:
        """Cleanup resources"""
        ...


class BaseTeam(ABC):
    """Base team implementation"""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize team"""
        ...

    @abstractmethod
    async def execute(self, task: str, **kwargs: Any) -> TeamResult:
        """Execute team task"""
        ...

    @abstractmethod
    async def add_agent(self, agent: TeamAgent) -> None:
        """Add agent to team"""
        ...

    @abstractmethod
    async def add_tool(self, tool: TeamTool) -> None:
        """Add tool to team"""
        ...

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup team resources"""
        ... 