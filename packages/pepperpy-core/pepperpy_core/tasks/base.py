"""Base task management implementation"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional
from uuid import UUID, uuid4

from ..base.types import JsonDict
from ..utils.datetime import utc_now


class TaskStatus(str, Enum):
    """Task status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Task definition"""

    id: UUID = field(default_factory=uuid4)
    name: str = ""
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=utc_now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Any = None
    error: Optional[Exception] = None
    metadata: JsonDict = field(default_factory=dict)


class TaskManager:
    """Task manager implementation"""

    def __init__(self) -> None:
        self._tasks: Dict[UUID, Task] = {}
        self._running: Dict[UUID, asyncio.Task[Any]] = {}

    async def create_task(self, name: str, func: Callable[..., Any], **metadata: Any) -> Task:
        """Create new task"""
        task = Task(name=name, metadata=metadata)
        self._tasks[task.id] = task
        return task

    async def start_task(self, task_id: UUID) -> None:
        """Start task execution"""
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if task.status != TaskStatus.PENDING:
            raise ValueError(f"Task {task_id} already started")

        task.status = TaskStatus.RUNNING
        task.started_at = utc_now()

    async def complete_task(
        self, task_id: UUID, result: Any = None, error: Optional[Exception] = None
    ) -> None:
        """Complete task execution"""
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        task.completed_at = utc_now()
        task.result = result
        task.error = error
        task.status = TaskStatus.COMPLETED if not error else TaskStatus.FAILED

    async def cancel_task(self, task_id: UUID) -> None:
        """Cancel task execution"""
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if task.status == TaskStatus.RUNNING:
            running = self._running.get(task_id)
            if running:
                running.cancel()
                try:
                    await running
                except asyncio.CancelledError:
                    pass

        task.status = TaskStatus.CANCELLED
        task.completed_at = utc_now()

    def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID"""
        return self._tasks.get(task_id)

    def list_tasks(self, status: Optional[TaskStatus] = None) -> list[Task]:
        """List all tasks"""
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks


__all__ = [
    "Task",
    "TaskManager",
    "TaskStatus",
]
