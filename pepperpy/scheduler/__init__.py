"""Task scheduling and background jobs management."""
from typing import Any, Dict, Optional, Callable, List, Union
from dataclasses import dataclass, field
import asyncio
from datetime import datetime, timedelta
import uuid
from enum import Enum
from abc import ABC, abstractmethod
from loguru import logger

class JobStatus(Enum):
    """Job execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class JobPriority(Enum):
    """Job priority levels."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class JobConfig:
    """Configuration for a scheduled job."""
    interval: Optional[timedelta] = None
    cron: Optional[str] = None
    max_retries: int = 3
    retry_delay: timedelta = timedelta(seconds=60)
    timeout: Optional[float] = None
    priority: JobPriority = JobPriority.NORMAL

@dataclass
class JobResult:
    """Result of a job execution."""
    success: bool
    result: Any = None
    error: Optional[Exception] = None
    execution_time: float = 0.0
    retries: int = 0

@dataclass
class Job:
    """Represents a scheduled job."""
    id: str
    name: str
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    config: JobConfig = field(default_factory=JobConfig)
    status: JobStatus = JobStatus.PENDING
    next_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    last_result: Optional[JobResult] = None

class JobStore(ABC):
    """Abstract base class for job storage."""
    
    @abstractmethod
    async def add_job(self, job: Job) -> None:
        """Add a job to the store."""
        pass
    
    @abstractmethod
    async def get_job(self, job_id: str) -> Optional[Job]:
        """Get a job by ID."""
        pass
    
    @abstractmethod
    async def update_job(self, job: Job) -> None:
        """Update a job's status and results."""
        pass
    
    @abstractmethod
    async def remove_job(self, job_id: str) -> None:
        """Remove a job from the store."""
        pass
    
    @abstractmethod
    async def get_pending_jobs(self) -> List[Job]:
        """Get all pending jobs."""
        pass

class MemoryJobStore(JobStore):
    """In-memory job storage."""
    
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
    
    async def add_job(self, job: Job) -> None:
        self.jobs[job.id] = job
    
    async def get_job(self, job_id: str) -> Optional[Job]:
        return self.jobs.get(job_id)
    
    async def update_job(self, job: Job) -> None:
        self.jobs[job.id] = job
    
    async def remove_job(self, job_id: str) -> None:
        self.jobs.pop(job_id, None)
    
    async def get_pending_jobs(self) -> List[Job]:
        return [
            job for job in self.jobs.values()
            if job.status == JobStatus.PENDING
        ]

class Scheduler:
    """Task scheduler and job manager."""
    
    def __init__(
        self,
        job_store: Optional[JobStore] = None,
        max_workers: int = 10
    ):
        self.job_store = job_store or MemoryJobStore()
        self.max_workers = max_workers
        self._running = False
        self._tasks: Dict[str, asyncio.Task] = {}
        self._semaphore = asyncio.Semaphore(max_workers)
    
    async def start(self) -> None:
        """Start the scheduler."""
        self._running = True
        asyncio.create_task(self._run_scheduler())
        logger.info("Scheduler started")
    
    async def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        for task in self._tasks.values():
            task.cancel()
        await asyncio.gather(*self._tasks.values(), return_exceptions=True)
        logger.info("Scheduler stopped")
    
    async def schedule(
        self,
        func: Callable,
        *args,
        name: Optional[str] = None,
        **kwargs
    ) -> Job:
        """Schedule a new job."""
        job_config = kwargs.pop("config", JobConfig())
        job_id = str(uuid.uuid4())
        
        job = Job(
            id=job_id,
            name=name or func.__name__,
            func=func,
            args=args,
            kwargs=kwargs,
            config=job_config,
            next_run=self._calculate_next_run(job_config)
        )
        
        await self.job_store.add_job(job)
        logger.info(f"Scheduled job {job.name} ({job.id})")
        return job
    
    async def cancel_job(self, job_id: str) -> None:
        """Cancel a scheduled job."""
        if job := await self.job_store.get_job(job_id):
            job.status = JobStatus.CANCELLED
            await self.job_store.update_job(job)
            
            if task := self._tasks.get(job_id):
                task.cancel()
                
            logger.info(f"Cancelled job {job.name} ({job.id})")
    
    async def get_job_status(self, job_id: str) -> Optional[JobStatus]:
        """Get the current status of a job."""
        if job := await self.job_store.get_job(job_id):
            return job.status
        return None
    
    async def get_job_result(self, job_id: str) -> Optional[JobResult]:
        """Get the result of a completed job."""
        if job := await self.job_store.get_job(job_id):
            return job.last_result
        return None
    
    async def _run_scheduler(self) -> None:
        """Main scheduler loop."""
        while self._running:
            try:
                now = datetime.now()
                pending_jobs = await self.job_store.get_pending_jobs()
                
                for job in pending_jobs:
                    if job.next_run and job.next_run <= now:
                        await self._execute_job(job)
                
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
    
    async def _execute_job(self, job: Job) -> None:
        """Execute a job."""
        async with self._semaphore:
            start_time = datetime.now()
            job.status = JobStatus.RUNNING
            await self.job_store.update_job(job)
            
            try:
                if asyncio.iscoroutinefunction(job.func):
                    result = await job.func(*job.args, **job.kwargs)
                else:
                    result = job.func(*job.args, **job.kwargs)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                job.last_result = JobResult(
                    success=True,
                    result=result,
                    execution_time=execution_time
                )
                job.status = JobStatus.COMPLETED
                
            except Exception as e:
                logger.error(f"Job {job.name} failed: {str(e)}")
                job.last_result = JobResult(
                    success=False,
                    error=e,
                    execution_time=(datetime.now() - start_time).total_seconds()
                )
                
                if job.last_result.retries < job.config.max_retries:
                    job.status = JobStatus.PENDING
                    job.next_run = datetime.now() + job.config.retry_delay
                    job.last_result.retries += 1
                else:
                    job.status = JobStatus.FAILED
            
            finally:
                job.last_run = start_time
                if job.config.interval and job.status != JobStatus.FAILED:
                    job.next_run = datetime.now() + job.config.interval
                    job.status = JobStatus.PENDING
                
                await self.job_store.update_job(job)
    
    def _calculate_next_run(self, config: JobConfig) -> Optional[datetime]:
        """Calculate next run time based on configuration."""
        if config.interval:
            return datetime.now() + config.interval
        elif config.cron:
            # TODO: Implement cron expression parsing
            return datetime.now()
        return datetime.now()

# Convenience functions
def create_scheduler(**kwargs) -> Scheduler:
    """Create a new scheduler instance."""
    return Scheduler(**kwargs) 