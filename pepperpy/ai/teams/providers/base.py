"""Base provider for multi-agent frameworks"""

from abc import ABC, abstractmethod
from typing import Any, Protocol

from pepperpy.core.module import BaseModule

from ..interfaces import TeamAgent, TeamTool
from ..types import TeamConfig, TeamResult


class TeamProvider(Protocol):
    """Protocol for team providers"""

    async def initialize(self) -> None:
        """Initialize provider"""
        ...

    async def execute(self, task: str, **kwargs: Any) -> TeamResult:
        """Execute team task"""
        ...

    async def add_agent(self, agent: TeamAgent) -> None:
        """Add agent to team"""
        ...

    async def add_tool(self, tool: TeamTool) -> None:
        """Add tool to team"""
        ...

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        ...


class BaseTeamProvider(BaseModule, ABC):
    """Base class for team providers"""

    def __init__(self, config: TeamConfig) -> None:
        self.config = config
        self._agents: list[TeamAgent] = []
        self._tools: list[TeamTool] = []
        self._initialized = False

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""
        if self._initialized:
            return

        # Initialize agents
        for agent in self._agents:
            await agent.initialize()

        # Initialize tools
        for tool in self._tools:
            await tool.initialize()

        self._initialized = True

    @abstractmethod
    async def execute(self, task: str, **kwargs: Any) -> TeamResult:
        """Execute team task"""
        if not self._initialized:
            await self.initialize()

    async def add_agent(self, agent: TeamAgent) -> None:
        """Add agent to team"""
        self._agents.append(agent)
        if self._initialized:
            await agent.initialize()

    async def add_tool(self, tool: TeamTool) -> None:
        """Add tool to team"""
        self._tools.append(tool)
        if self._initialized:
            await tool.initialize()

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        for agent in self._agents:
            await agent.cleanup()
        for tool in self._tools:
            await tool.cleanup()
        self._initialized = False
