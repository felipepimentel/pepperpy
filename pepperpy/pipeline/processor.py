"""Data pipeline processor implementation."""
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum
import asyncio
from ..core.config import Config
from ..logging import get_logger

T = TypeVar('T')
R = TypeVar('R')

logger = get_logger()

class PipelineStage(Generic[T, R]):
    """Single stage in a data pipeline."""
    
    def __init__(
        self,
        name: str,
        processor: Callable[[T], R],
        error_handler: Optional[Callable[[Exception], R]] = None
    ):
        self.name = name
        self.processor = processor
        self.error_handler = error_handler
    
    async def process(self, data: T) -> R:
        """Process data through this stage."""
        try:
            if asyncio.iscoroutinefunction(self.processor):
                return await self.processor(data)
            return self.processor(data)
        except Exception as e:
            if self.error_handler:
                return self.error_handler(e)
            raise

class Pipeline:
    """Data processing pipeline."""
    
    def __init__(self, name: str, config: Optional[Config] = None):
        self.name = name
        self.config = config or Config()
        self.stages: List[PipelineStage] = []
    
    def add_stage(
        self,
        name: str,
        processor: Callable,
        error_handler: Optional[Callable] = None
    ) -> 'Pipeline':
        """Add processing stage to pipeline."""
        self.stages.append(PipelineStage(name, processor, error_handler))
        return self
    
    async def process(self, initial_data: Any) -> Any:
        """Process data through all pipeline stages."""
        current_data = initial_data
        
        for stage in self.stages:
            try:
                logger.debug(f"Processing stage: {stage.name}")
                current_data = await stage.process(current_data)
                logger.debug(f"Stage {stage.name} completed")
            except Exception as e:
                logger.error(f"Error in pipeline {self.name} at stage {stage.name}: {str(e)}")
                raise
        
        return current_data

def create_pipeline(name: str) -> Pipeline:
    """Create a new data pipeline."""
    return Pipeline(name) 