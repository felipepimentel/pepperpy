"""Pipeline type definitions"""

from typing import Any, Sequence, TypeVar

from pydantic import BaseModel, Field

from pepperpy.ai.config.provider import ProviderConfig as AIConfig
from pepperpy.core.types import JsonDict


class PipelineConfig(BaseModel):
    """Pipeline configuration"""

    name: str
    ai_config: AIConfig
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True


class PipelineResult(BaseModel):
    """Pipeline execution result"""

    success: bool
    output: Any
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True


class PipelineStep(BaseModel):
    """Pipeline step definition"""

    name: str
    handler: str
    config: dict[str, Any] = Field(default_factory=dict)
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True


class Pipeline(BaseModel):
    """Pipeline definition"""

    name: str
    steps: Sequence[PipelineStep]
    config: PipelineConfig
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True


# Type variables for pipeline input/output
InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")
