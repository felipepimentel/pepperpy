"""Example of task scheduling and background jobs."""
import asyncio
from datetime import timedelta
from pepperpy.scheduler import (
    create_scheduler,
    JobConfig,
    JobPriority
)

async def long_running_task(name: str) -> str:
    """Simulate a long-running task."""
    print(f"Starting task: {name}")
    await asyncio.sleep(2)  # Simulate work
    print(f"Completed task: {name}")
    return f"Result from {name}"

async def failing_task() -> None:
    """Simulate a failing task."""
    raise ValueError("Task failed intentionally")

async def demonstrate_scheduler():
    """Demonstrate scheduler functionality."""
    # Create scheduler
    scheduler = create_scheduler(max_workers=3)
    await scheduler.start()
    
    try:
        # Schedule recurring task
        recurring_job = await scheduler.schedule(
            long_running_task,
            "Recurring Task",
            config=JobConfig(
                interval=timedelta(seconds=5),
                priority=JobPriority.HIGH
            )
        )
        print(f"Scheduled recurring job: {recurring_job.id}")
        
        # Schedule one-time task
        onetime_job = await scheduler.schedule(
            long_running_task,
            "One-time Task",
            config=JobConfig(
                max_retries=2,
                priority=JobPriority.NORMAL
            )
        )
        print(f"Scheduled one-time job: {onetime_job.id}")
        
        # Schedule failing task
        failing_job = await scheduler.schedule(
            failing_task,
            config=JobConfig(
                max_retries=3,
                retry_delay=timedelta(seconds=2)
            )
        )
        print(f"Scheduled failing job: {failing_job.id}")
        
        # Wait and monitor jobs
        for _ in range(20):
            recurring_status = await scheduler.get_job_status(recurring_job.id)
            onetime_status = await scheduler.get_job_status(onetime_job.id)
            failing_status = await scheduler.get_job_status(failing_job.id)
            
            print(f"\nJob Status:")
            print(f"Recurring: {recurring_status}")
            print(f"One-time: {onetime_status}")
            print(f"Failing: {failing_status}")
            
            await asyncio.sleep(1)
            
        # Cancel recurring job
        await scheduler.cancel_job(recurring_job.id)
        
        # Get results
        onetime_result = await scheduler.get_job_result(onetime_job.id)
        if onetime_result:
            print(f"\nOne-time job result: {onetime_result.result}")
            print(f"Execution time: {onetime_result.execution_time:.2f}s")
        
        failing_result = await scheduler.get_job_result(failing_job.id)
        if failing_result:
            print(f"\nFailing job error: {failing_result.error}")
            print(f"Retries: {failing_result.retries}")
        
    finally:
        await scheduler.stop()

if __name__ == "__main__":
    asyncio.run(demonstrate_scheduler()) 