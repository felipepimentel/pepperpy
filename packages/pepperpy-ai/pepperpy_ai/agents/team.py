"""Team agent implementations."""

from typing import Any

from ..ai_types import AIMessage, AIResponse
from .base import BaseAgent
from .team_types import TeamConfig, TeamMessage
from .types import AgentConfig, AgentRole


class TeamAgent(BaseAgent):
    """Team agent implementation."""

    def __init__(self, config: AgentConfig) -> None:
        """Initialize agent."""
        super().__init__(config)
        self._team_config: TeamConfig | None = None

    async def _setup(self) -> None:
        """Setup agent resources."""
        pass

    async def _teardown(self) -> None:
        """Teardown agent resources."""
        pass

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute team task."""
        self._ensure_initialized()
        return AIResponse(
            content=f"Team task: {task}",
            messages=[AIMessage(role=AgentRole.PLANNER, content=task)],
        )

    def _ensure_initialized(self) -> None:
        """Ensure agent is initialized."""
        if not self.is_initialized:
            raise RuntimeError("Agent not initialized")

    async def coordinate(self, messages: list[TeamMessage]) -> AIResponse:
        """Coordinate team communication.

        Args:
            messages: Team messages to coordinate

        Returns:
            Coordination response
        """
        self._ensure_initialized()
        return AIResponse(
            content="Team coordination",
            messages=[
                AIMessage(role=AgentRole.PLANNER, content=msg.content)
                for msg in messages
            ],
        )


class TeamCoordinator(BaseAgent):
    """Team coordinator implementation."""

    def __init__(self, config: AgentConfig) -> None:
        """Initialize coordinator."""
        super().__init__(config)
        self._team_config: TeamConfig | None = None

    async def _setup(self) -> None:
        """Setup coordinator resources."""
        pass

    async def _teardown(self) -> None:
        """Teardown coordinator resources."""
        pass

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute coordination task."""
        self._ensure_initialized()
        return AIResponse(
            content=f"Coordination task: {task}",
            messages=[AIMessage(role=AgentRole.PLANNER, content=task)],
        )

    def _ensure_initialized(self) -> None:
        """Ensure coordinator is initialized."""
        if not self.is_initialized:
            raise RuntimeError("Coordinator not initialized")

    async def assign_tasks(self, tasks: list[str]) -> AIResponse:
        """Assign tasks to team members.

        Args:
            tasks: Tasks to assign

        Returns:
            Task assignment response
        """
        self._ensure_initialized()
        return AIResponse(
            content="Task assignments",
            messages=[
                AIMessage(role=AgentRole.PLANNER, content=task) for task in tasks
            ],
        )
