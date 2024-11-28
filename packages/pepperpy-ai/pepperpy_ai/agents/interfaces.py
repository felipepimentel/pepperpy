"""AI agent interfaces"""

from typing import Protocol, runtime_checkable

from bko.ai.types import AIResponse


@runtime_checkable
class ProjectManagerAgent(Protocol):
    """Project manager agent interface"""

    async def initialize(self) -> None: ...

    async def cleanup(self) -> None: ...

    async def plan(self, task: str) -> AIResponse: ...

    async def coordinate(self, tasks: list[str]) -> AIResponse: ...


@runtime_checkable
class QAAgent(Protocol):
    """QA agent interface"""

    async def initialize(self) -> None: ...

    async def cleanup(self) -> None: ...

    async def test(self, code: str) -> AIResponse: ...

    async def plan_tests(self, task: str) -> AIResponse: ...