"""Task manager module."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from .status import TaskStatus


@dataclass
class Task:
    """Task data class."""

    id: UUID
    name: str
    func: Callable[[], Any]
    status: TaskStatus = TaskStatus.PENDING
    result: Any | None = None
    error: Exception | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class TaskManager:
    """Task manager implementation."""

    def __init__(self) -> None:
        """Initialize task manager."""
        self._tasks: dict[UUID, Task] = {}

    async def create_task(
        self, name: str, func: Callable[[], Any], **metadata: Any
    ) -> Task:
        """Create a new task."""
        task = Task(id=uuid4(), name=name, func=func, metadata=metadata)
        self._tasks[task.id] = task
        return task

    async def start_task(self, task_id: UUID) -> None:
        """Start task execution."""
        task = self._tasks[task_id]
        task.status = TaskStatus.RUNNING

    async def complete_task(
        self, task_id: UUID, result: Any | None = None, error: Exception | None = None
    ) -> None:
        """Complete task execution."""
        task = self._tasks[task_id]
        if error:
            task.status = TaskStatus.FAILED
            task.error = error
        else:
            task.status = TaskStatus.COMPLETED
            task.result = result

    async def cancel_task(self, task_id: UUID) -> None:
        """Cancel task execution."""
        task = self._tasks[task_id]
        task.status = TaskStatus.CANCELLED
