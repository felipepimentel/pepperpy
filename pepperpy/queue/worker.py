"""Background job processing system."""
from typing import Any, Callable, Dict, Optional
import asyncio
from datetime import datetime
import aio_pika
from pydantic import BaseModel

class JobConfig(BaseModel):
    """Job configuration."""
    queue_url: str = "amqp://guest:guest@localhost/"
    queue_name: str = "pepperpy_jobs"
    max_retries: int = 3
    retry_delay: int = 60

class JobWorker:
    """Background job worker."""
    
    def __init__(self, config: Optional[JobConfig] = None):
        self.config = config or JobConfig()
        self.handlers: Dict[str, Callable] = {}
        self._connection = None
        self._channel = None
        
    async def connect(self):
        """Establish connection to message broker."""
        self._connection = await aio_pika.connect_robust(self.config.queue_url)
        self._channel = await self._connection.channel()
        await self._channel.declare_queue(self.config.queue_name, durable=True)
    
    def register_handler(self, job_type: str, handler: Callable):
        """Register job handler."""
        self.handlers[job_type] = handler
    
    async def process_job(self, message: aio_pika.IncomingMessage):
        """Process incoming job."""
        async with message.process():
            job_data = message.body.decode()
            job = JobMessage.parse_raw(job_data)
            
            try:
                handler = self.handlers[job.type]
                await handler(job.payload)
            except Exception as e:
                if job.retries < self.config.max_retries:
                    # Requeue with delay
                    await asyncio.sleep(self.config.retry_delay)
                    await self.enqueue(
                        job.type,
                        job.payload,
                        retries=job.retries + 1
                    )
                else:
                    # Log failure
                    print(f"Job failed after {job.retries} retries: {e}")
    
    async def start(self):
        """Start processing jobs."""
        if not self._connection:
            await self.connect()
        
        queue = await self._channel.declare_queue(
            self.config.queue_name,
            durable=True
        )
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await self.process_job(message) 