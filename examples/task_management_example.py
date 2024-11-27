"""Task management example"""

import asyncio
import random
from dataclasses import dataclass
from typing import Any

from pepperpy_core.exceptions import ModuleError
from pepperpy_core.module import BaseModule
from pepperpy_core.tasks import TaskManager, TaskStatus
from pepperpy_core.types import JsonDict


@dataclass
class WorkerConfig:
    """Worker configuration"""

    name: str
    settings: JsonDict
    num_workers: int = 3
    task_timeout: float = 5.0


class WorkerModule(BaseModule[WorkerConfig]):
    """Worker module implementation"""

    def __init__(self, config: WorkerConfig) -> None:
        super().__init__(config)
        self._task_manager = TaskManager()
        self._workers: list[asyncio.Task[None]] = []

    async def _initialize(self) -> None:
        """Initialize workers"""
        print(f"Starting {self.config.num_workers} workers...")
        for i in range(self.config.num_workers):
            worker = asyncio.create_task(self._worker_loop(i))
            self._workers.append(worker)
        self._metadata["workers_started"] = True

    async def _cleanup(self) -> None:
        """Cleanup workers"""
        print("Stopping workers...")
        for worker in self._workers:
            worker.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()

    async def _worker_loop(self, worker_id: int) -> None:
        """Worker loop"""
        while True:
            try:
                # Simulate work
                await asyncio.sleep(random.uniform(0.1, 0.5))
                print(f"Worker {worker_id} processed task")
            except asyncio.CancelledError:
                print(f"Worker {worker_id} stopped")
                break
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")

    async def submit_task(self, name: str, func: Any) -> str:
        """Submit task for processing"""
        self._ensure_initialized()
        try:
            task = await self._task_manager.create_task(
                name, func, timeout=self.config.task_timeout
            )
            return task.id
        except Exception as e:
            raise ModuleError("Failed to submit task", cause=e)

    async def get_task_status(self, task_id: str) -> TaskStatus:
        """Get task status"""
        self._ensure_initialized()
        return await self._task_manager.get_task_status(task_id)


async def main() -> None:
    """Run worker example"""
    # Create module
    config = WorkerConfig(
        name="worker_pool", settings={"debug": True}, num_workers=3, task_timeout=5.0
    )
    module = WorkerModule(config)

    try:
        # Initialize
        await module.initialize()

        # Submit tasks
        async def example_task(delay: float) -> str:
            await asyncio.sleep(delay)
            return f"Task completed after {delay}s"

        task_ids = []
        for i in range(5):
            task_id = await module.submit_task(
                f"task_{i}", lambda: example_task(random.uniform(0.5, 2.0))
            )
            task_ids.append(task_id)
            print(f"Submitted task {task_id}")

        # Monitor tasks
        while task_ids:
            for task_id in task_ids[:]:
                status = await module.get_task_status(task_id)
                if status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
                    print(f"Task {task_id} finished with status {status}")
                    task_ids.remove(task_id)
            await asyncio.sleep(0.5)

    finally:
        # Cleanup
        await module.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
