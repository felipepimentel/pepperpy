"""Test task functionality."""

from dataclasses import dataclass
from typing import Any

import pytest
from pepperpy_core.tasks import Task


@dataclass
class TaskResult:
    """Task result data."""

    name: str
    success: bool
    message: str


class TestTask(Task):
    """Test task implementation."""

    def __init__(self) -> None:
        """Initialize test task."""
        self.results: list[TaskResult] = []

    async def run(self, *args: Any, **kwargs: Any) -> TaskResult:
        """Run test task."""
        result = TaskResult(
            name=self.__class__.__name__,
            success=True,
            message="Test task completed",
        )
        self.results.append(result)
        return result


@pytest.fixture
def test_task() -> TestTask:
    """Create test task fixture."""
    return TestTask()


@pytest.mark.asyncio
async def test_task_run(test_task: TestTask) -> None:
    """Test task run."""
    result = await test_task.run()
    assert result.success
    assert result.message == "Test task completed"
    assert len(test_task.results) == 1
