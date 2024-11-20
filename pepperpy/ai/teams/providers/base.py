"""Base team provider implementation"""

from typing import Any, Protocol

from pepperpy.core.module import BaseModule

from ..types import TeamConfig, TeamResult


class TeamProvider(Protocol):
    """Team provider protocol"""

    async def initialize(self) -> None:
        """Initialize provider"""
        ...

    async def execute(self, task: str, **kwargs: Any) -> TeamResult:
        """Execute team task"""
        ...

    async def cleanup(self) -> None:
        """Cleanup provider"""
        ...


class BaseTeamProvider(BaseModule[TeamConfig]):
    """Base team provider implementation"""

    def __init__(self, config: TeamConfig) -> None:
        super().__init__(config)

    async def _initialize(self) -> None:
        """Initialize provider"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        pass
