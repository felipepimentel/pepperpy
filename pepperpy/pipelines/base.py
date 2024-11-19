"""Base pipeline implementation"""

from dataclasses import dataclass, field
from typing import Any

from pepperpy.core.module import BaseModule, ModuleMetadata
from pepperpy.core.providers import AIProvider

from .types import PipelineConfig


@dataclass
class BasePipeline(BaseModule):
    """Base class for processing pipelines"""

    metadata: ModuleMetadata = field(init=False)
    config: PipelineConfig = field(default_factory=PipelineConfig)
    _provider: AIProvider | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        """Post initialization"""
        self.metadata = ModuleMetadata(
            name=self.__class__.__name__,
            version="0.1.0",
            description="Base pipeline implementation",
            config={"pipeline": self.config},
        )

    async def initialize(self) -> None:
        """Initialize pipeline resources"""
        if self.config.ai_config:
            self._provider = await AIProvider.create(self.config.ai_config)

    async def cleanup(self) -> None:
        """Cleanup pipeline resources"""
        if self._provider:
            await self._provider.cleanup()

    async def process(self, *args: Any, **kwargs: Any) -> Any:
        """Process pipeline input"""
        raise NotImplementedError("Pipeline must implement process method")
