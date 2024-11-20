"""Pipeline type definitions"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar

from pepperpy.ai.config import AIConfig
from pepperpy.core.types import JsonDict, ModuleConfig

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class PipelineType(str, Enum):
    """Pipeline types"""

    TEXT = "text"
    DATA = "data"
    VECTOR = "vector"
    CUSTOM = "custom"


@dataclass
class PipelineConfig(ModuleConfig):
    """Pipeline configuration"""

    pipeline_type: PipelineType = PipelineType.CUSTOM
    ai_config: AIConfig | None = None
    steps: list[str] = field(default_factory=list)
    parallel: bool = False
    input_type: str | None = None
    output_type: str | None = None


@dataclass
class PipelineResult:
    """Pipeline execution result"""

    success: bool
    output: Any
    metadata: JsonDict = field(default_factory=dict) 