"""Task scheduling and background jobs."""
from typing import Optional, Union, Callable
from datetime import datetime, timedelta
import asyncio
import aiocron
from croniter import croniter

class TaskScheduler:
    """Schedule and manage background tasks."""
    
    def __init__(self):
        self.tasks = {}
        self.running = False
        
    async def add_task(
        self,
        func: Callable,
        schedule: Union[str, int, timedelta],
        name: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Add a new task.
        
        Args:
            func: Function to execute
            schedule: Cron expression, interval in seconds, or timedelta
            name: Task name (optional)
            **kwargs: Arguments for the function
        """
        task_id = name or f"task_{len(self.tasks)}"
        
        if isinstance(schedule, str) and croniter.is_valid(schedule):
            # Cron schedule
            self.tasks[task_id] = aiocron.crontab(schedule, func=func, **kwargs)
        else:
            # Interval schedule
            interval = schedule if isinstance(schedule, int) else schedule.total_seconds()
            
            async def run_periodic():
                while self.running:
                    try:
                        await func(**kwargs)
                    except Exception as e:
                        print(f"Error in task {task_id}: {e}")
                    await asyncio.sleep(interval)
                    
            self.tasks[task_id] = asyncio.create_task(run_periodic())
            
        return task_id
        
    async def start(self):
        """Start the scheduler."""
        self.running = True
        
    async def stop(self):
        """Stop the scheduler."""
        self.running = False
        for task in self.tasks.values():
            if hasattr(task, "stop"):
                await task.stop()
            else:
                task.cancel() 