"""Task management implementation"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from .exceptions import CoreError
from .logging import get_logger
from .module import BaseModule, ModuleMetadata


class TaskError(CoreError):
    """Task management error"""

    pass


class TaskStatus(Enum):
    """Task execution status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskConfig:
    """Configuration for task scheduler"""

    max_concurrent: int = 10
    default_timeout: float = 300.0  # 5 minutes
    retry_count: int = 3
    retry_delay: float = 1.0
    preserve_completed: bool = True
    max_history: int = 1000
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskInfo:
    """Task execution information"""

    id: str
    name: str
    status: TaskStatus
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[Exception] = None
    result: Any = None
    retries: int = 0
    timeout: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TaskScheduler(BaseModule):
    """Async task scheduler"""

    def __init__(self, config: Optional[TaskConfig] = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="task_scheduler",
            version="1.0.0",
            description="Async task scheduling",
            dependencies=[],
            config=config.__dict__ if config else TaskConfig().__dict__,
        )
        self._tasks: Dict[str, TaskInfo] = {}
        self._running: Dict[str, asyncio.Task] = {}
        self._queue: asyncio.Queue = asyncio.Queue()
        self._worker: Optional[asyncio.Task] = None
        self._running = False
        self._listeners: List[Callable] = []
        self._logger = get_logger(__name__)

    async def _setup(self) -> None:
        """Initialize task scheduler"""
        try:
            self._running = True
            self._worker = asyncio.create_task(self._process_queue())
        except Exception as e:
            raise TaskError("Failed to initialize task scheduler", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup task scheduler"""
        try:
            self._running = False
            if self._worker:
                await self._worker
                self._worker = None

            # Cancel running tasks
            for task in self._running.values():
                task.cancel()
            await asyncio.gather(*self._running.values(), return_exceptions=True)
            self._running.clear()

        except Exception as e:
            await self._logger.error(f"Error during cleanup: {str(e)}")

    async def schedule(
        self,
        name: str,
        coroutine: Callable,
        *args,
        timeout: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> str:
        """Schedule task for execution"""
        task_id = str(uuid.uuid4())
        info = TaskInfo(
            id=task_id,
            name=name,
            status=TaskStatus.PENDING,
            timeout=timeout or self.config.get("default_timeout"),
            metadata=metadata or {},
        )
        self._tasks[task_id] = info

        await self._queue.put((task_id, coroutine, args, kwargs))
        await self._notify_listeners("scheduled", info)
        return task_id

    async def schedule_periodic(
        self,
        name: str,
        coroutine: Callable,
        interval: Union[int, float, timedelta],
        *args,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> str:
        """Schedule periodic task"""
        if isinstance(interval, timedelta):
            interval = interval.total_seconds()

        async def periodic_wrapper():
            while True:
                try:
                    await coroutine(*args, **kwargs)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    await self._logger.error(f"Error in periodic task {name}: {str(e)}")
                await asyncio.sleep(interval)

        return await self.schedule(
            name,
            periodic_wrapper,
            metadata={"periodic": True, "interval": interval, **(metadata or {})},
        )

    async def cancel(self, task_id: str) -> None:
        """Cancel scheduled or running task"""
        if task_id in self._running:
            self._running[task_id].cancel()
            info = self._tasks[task_id]
            info.status = TaskStatus.CANCELLED
            info.completed_at = datetime.utcnow()
            await self._notify_listeners("cancelled", info)

    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """Get task information"""
        return self._tasks.get(task_id)

    def get_tasks(
        self, status: Optional[TaskStatus] = None, name: Optional[str] = None
    ) -> List[TaskInfo]:
        """Get tasks with optional filters"""
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        if name:
            tasks = [t for t in tasks if t.name == name]
        return tasks

    def add_listener(self, listener: Callable) -> None:
        """Add task event listener"""
        self._listeners.append(listener)

    def remove_listener(self, listener: Callable) -> None:
        """Remove task event listener"""
        self._listeners.remove(listener)

    async def _process_queue(self) -> None:
        """Process task queue"""
        while self._running:
            try:
                # Wait for available slot
                while len(self._running) >= self.config.get("max_concurrent"):
                    await asyncio.sleep(0.1)

                # Get next task
                task_id, coroutine, args, kwargs = await self._queue.get()

                # Update status
                info = self._tasks[task_id]
                info.status = TaskStatus.RUNNING
                info.started_at = datetime.utcnow()
                await self._notify_listeners("started", info)

                # Create and start task with timeout
                task = asyncio.create_task(self._run_task(task_id, coroutine, *args, **kwargs))
                self._running[task_id] = task

                self._queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                await self._logger.error(f"Error processing task queue: {str(e)}")

    async def _run_task(self, task_id: str, coroutine: Callable, *args, **kwargs) -> None:
        """Run task with timeout and retry"""
        info = self._tasks[task_id]
        try:
            # Run with timeout
            result = await asyncio.wait_for(coroutine(*args, **kwargs), timeout=info.timeout)
            info.status = TaskStatus.COMPLETED
            info.result = result

        except asyncio.TimeoutError:
            info.status = TaskStatus.FAILED
            info.error = TaskError("Task timeout exceeded")

        except asyncio.CancelledError:
            info.status = TaskStatus.CANCELLED

        except Exception as e:
            info.status = TaskStatus.FAILED
            info.error = e

            # Retry if needed
            if info.retries < self.config.get("retry_count") and not isinstance(
                e, asyncio.CancelledError
            ):
                info.retries += 1
                await asyncio.sleep(self.config.get("retry_delay") * (2 ** (info.retries - 1)))
                await self._queue.put((task_id, coroutine, args, kwargs))
                return

        finally:
            info.completed_at = datetime.utcnow()
            if task_id in self._running:
                del self._running[task_id]

            # Clean up if needed
            if not self.config.get("preserve_completed") and info.status in (
                TaskStatus.COMPLETED,
                TaskStatus.CANCELLED,
            ):
                del self._tasks[task_id]

            await self._notify_listeners("completed", info)

    async def _notify_listeners(self, event: str, task: TaskInfo) -> None:
        """Notify task event listeners"""
        for listener in self._listeners:
            try:
                await listener(event, task)
            except Exception as e:
                await self._logger.error(f"Error in task listener: {str(e)}")


# Global task scheduler instance
scheduler = TaskScheduler()
