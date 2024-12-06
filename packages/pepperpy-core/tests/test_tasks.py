"""Task tests."""

from collections.abc import AsyncGenerator

import pytest

from pepperpy_core.tasks import TaskManager


@pytest.fixture
async def task_manager() -> AsyncGenerator[TaskManager, None]:
    """Create task manager fixture."""
    manager = TaskManager()
    await manager.initialize()
    try:
        yield manager
    finally:
        await manager.cleanup()


@pytest.mark.asyncio
async def test_task_creation(task_manager: AsyncGenerator[TaskManager, None]) -> None:
    """Test task creation."""
    manager = await anext(task_manager)
    task = await manager.create_task("test_task", lambda: None)
    assert task is not None
    assert task.name == "test_task"


@pytest.mark.asyncio
async def test_task_execution(task_manager: AsyncGenerator[TaskManager, None]) -> None:
    """Test task execution."""
    manager = await anext(task_manager)
    result = []
    task = await manager.create_task("test_task", lambda: result.append(1))
    await task.execute()
    assert result == [1]


@pytest.mark.asyncio
async def test_task_failure(task_manager: AsyncGenerator[TaskManager, None]) -> None:
    """Test task failure."""
    manager = await anext(task_manager)
    task = await manager.create_task("test_task", lambda: 1 / 0)
    with pytest.raises(ZeroDivisionError):
        await task.execute()


@pytest.mark.asyncio
async def test_task_cancellation(
    task_manager: AsyncGenerator[TaskManager, None]
) -> None:
    """Test task cancellation."""
    manager = await anext(task_manager)
    task = await manager.create_task("test_task", lambda: None)
    await task.cancel()
    assert task.is_cancelled
