"""Workflow engine implementation."""
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from ..core.config import Config
from ..logging import get_logger

logger = get_logger()

class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """Workflow task definition."""
    name: str
    handler: Callable
    depends_on: List[str] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    timeout: Optional[int] = None
    
    async def execute(self, context: Dict[str, Any]) -> Any:
        """Execute task with retry logic."""
        while self.retry_count <= self.max_retries:
            try:
                if asyncio.iscoroutinefunction(self.handler):
                    return await self.handler(context)
                return self.handler(context)
            except Exception as e:
                self.retry_count += 1
                if self.retry_count > self.max_retries:
                    raise
                logger.warning(f"Task {self.name} failed, retrying ({self.retry_count}/{self.max_retries})")
                await asyncio.sleep(2 ** self.retry_count)  # Exponential backoff

class Workflow:
    """Workflow definition and execution."""
    
    def __init__(self, name: str, config: Optional[Config] = None):
        self.name = name
        self.config = config or Config()
        self.tasks: Dict[str, Task] = {}
        self.context: Dict[str, Any] = {}
        self.status = WorkflowStatus.PENDING
    
    def add_task(
        self,
        name: str,
        handler: Callable,
        depends_on: Optional[List[str]] = None,
        **task_options
    ) -> 'Workflow':
        """Add task to workflow."""
        self.tasks[name] = Task(
            name=name,
            handler=handler,
            depends_on=depends_on or [],
            **task_options
        )
        return self
    
    async def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute workflow tasks in order."""
        self.context = initial_context or {}
        self.status = WorkflowStatus.RUNNING
        completed_tasks = set()
        
        try:
            while len(completed_tasks) < len(self.tasks):
                ready_tasks = []
                
                # Find tasks ready to execute
                for name, task in self.tasks.items():
                    if name not in completed_tasks and all(
                        dep in completed_tasks for dep in task.depends_on
                    ):
                        ready_tasks.append(task)
                
                if not ready_tasks:
                    raise ValueError("Circular dependency detected")
                
                # Execute ready tasks in parallel
                results = await asyncio.gather(
                    *(task.execute(self.context) for task in ready_tasks),
                    return_exceptions=True
                )
                
                # Process results
                for task, result in zip(ready_tasks, results):
                    if isinstance(result, Exception):
                        raise result
                    self.context[task.name] = result
                    completed_tasks.add(task.name)
                    logger.info(f"Task {task.name} completed successfully")
            
            self.status = WorkflowStatus.COMPLETED
            return self.context
            
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            logger.error(f"Workflow {self.name} failed: {str(e)}")
            raise 