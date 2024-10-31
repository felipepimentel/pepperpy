"""Streaming support for async operations."""
from typing import AsyncGenerator, Any, Optional, Callable, TypeVar
from dataclasses import dataclass
from asyncio import Queue, create_task, Task
import asyncio

T = TypeVar('T')

@dataclass
class StreamingConfig:
    """Configuration for streaming operations."""
    buffer_size: int = 1024
    timeout: float = 30.0
    chunk_size: int = 64

class StreamProcessor:
    """Process streaming data with backpressure support."""
    
    def __init__(self, config: Optional[StreamingConfig] = None):
        self.config = config or StreamingConfig()
        self.queue: Queue = Queue(maxsize=self.config.buffer_size)
        self._processor_task: Optional[Task] = None
        
    async def process_stream(
        self,
        source: AsyncGenerator[T, None],
        processor: Callable[[T], Any],
        on_chunk: Optional[Callable[[Any], None]] = None
    ) -> AsyncGenerator[Any, None]:
        """Process a stream with backpressure."""
        try:
            self._processor_task = create_task(
                self._process_queue(processor, on_chunk)
            )
            
            async for chunk in source:
                await self.queue.put(chunk)
                
            await self.queue.put(None)  # Signal end of stream
            await self._processor_task
            
            while not self.queue.empty():
                result = await self.queue.get()
                if result is not None:
                    yield result
                    
        finally:
            if self._processor_task:
                self._processor_task.cancel()
                
    async def _process_queue(
        self,
        processor: Callable[[T], Any],
        on_chunk: Optional[Callable[[Any], None]]
    ):
        """Process items from the queue."""
        while True:
            chunk = await self.queue.get()
            if chunk is None:
                break
                
            try:
                result = processor(chunk)
                if on_chunk:
                    on_chunk(result)
                await self.queue.put(result)
            except Exception as e:
                await self.queue.put(e)
                break
            finally:
                self.queue.task_done() 