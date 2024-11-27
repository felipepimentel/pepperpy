"""Test task management functionality"""

from uuid import UUID

import pytest
from pepperpy_core.tasks import TaskManager, TaskStatus


@pytest.fixture
def task_manager() -> TaskManager:
    """Create task manager"""
    return TaskManager()


async def test_task_creation(task_manager: TaskManager) -> None:
    """Test task creation"""
    task = await task_manager.create_task("test_task", lambda: "result", test_meta="value")
    assert isinstance(task.id, UUID)
    assert task.name == "test_task"
    assert task.status == TaskStatus.PENDING
    assert task.metadata["test_meta"] == "value"


async def test_task_execution(task_manager: TaskManager) -> None:
    """Test task execution"""
    task = await task_manager.create_task("test_task", lambda: "result")
    await task_manager.start_task(task.id)
    assert task.status == TaskStatus.RUNNING
    await task_manager.complete_task(task.id, "success")
    assert task.status == TaskStatus.COMPLETED
    assert task.result == "success"


async def test_task_failure(task_manager: TaskManager) -> None:
    """Test task failure"""
    error = ValueError("test error")
    task = await task_manager.create_task("test_task", lambda: None)
    await task_manager.start_task(task.id)
    await task_manager.complete_task(task.id, error=error)
    assert task.status == TaskStatus.FAILED
    assert task.error == error


async def test_task_cancellation(task_manager: TaskManager) -> None:
    """Test task cancellation"""
    task = await task_manager.create_task("test_task", lambda: None)
    await task_manager.start_task(task.id)
    await task_manager.cancel_task(task.id)
    assert task.status == TaskStatus.CANCELLED
