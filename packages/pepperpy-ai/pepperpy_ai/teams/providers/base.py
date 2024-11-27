"""Base team provider implementation"""

from abc import ABC, abstractmethod
from typing import Any, Sequence

from bko.core.module import BaseModule

from ...types import AIResponse
from ..config import TeamConfig


class TeamProvider(BaseModule[TeamConfig], ABC):
    """Base team provider implementation"""

    def __init__(self, config: TeamConfig) -> None:
        super().__init__(config)
        self._initialized = False

    @abstractmethod
    async def execute_task(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute team task"""
        pass

    @abstractmethod
    async def get_team_members(self) -> Sequence[str]:
        """Get team member names"""
        pass

    @abstractmethod
    async def get_team_roles(self) -> dict[str, str]:
        """Get team member roles"""
        pass

    async def _initialize(self) -> None:
        """Initialize provider"""
        if self._initialized:
            return
        await self._setup()
        self._initialized = True

    async def _cleanup(self) -> None:
        """Cleanup provider resources"""
        if not self._initialized:
            return
        await self._teardown()
        self._initialized = False

    @abstractmethod
    async def _setup(self) -> None:
        """Setup provider resources"""
        pass

    @abstractmethod
    async def _teardown(self) -> None:
        """Teardown provider resources"""
        pass
