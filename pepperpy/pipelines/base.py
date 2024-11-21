"""Base pipeline implementation"""

from abc import ABC, abstractmethod
from typing import Generic

from pepperpy.core.module import BaseModule

from .types import InputT, OutputT, PipelineConfig, PipelineResult


class BasePipeline(Generic[InputT, OutputT], BaseModule[PipelineConfig], ABC):
    """Base pipeline implementation"""

    @abstractmethod
    async def process(self, input_data: InputT) -> PipelineResult[OutputT]:
        """Process pipeline input"""
        pass

    async def _initialize(self) -> None:
        """Initialize pipeline"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup pipeline resources"""
        pass
