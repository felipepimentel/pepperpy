"""Pipeline base implementation"""

from typing import Any

from pepperpy.core.module import BaseModule

from .types import PipelineConfig, PipelineResult


class BasePipeline(BaseModule[PipelineConfig]):
    """Base pipeline implementation"""

    def __init__(self, config: PipelineConfig) -> None:
        super().__init__(config)

    async def _initialize(self) -> None:
        """Initialize pipeline"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        pass

    async def execute(self, input_data: Any) -> PipelineResult:
        """Execute pipeline"""
        if not self._initialized:
            await self.initialize()
        raise NotImplementedError
