"""Pipeline module"""

from typing import Any

from .base import BasePipeline
from .exceptions import PipelineError
from .types import (
    InputT,
    OutputT,
    PipelineConfig,
    PipelineResult,
    PipelineType,
)
from .validation import validate_pipeline

__all__ = [
    # Base
    "BasePipeline",
    # Types
    "InputT",
    "OutputT",
    "PipelineConfig",
    "PipelineResult",
    "PipelineType",
    # Functions
    "validate_pipeline",
    # Exceptions
    "PipelineError",
]


def create_pipeline(
    name: str,
    pipeline_type: PipelineType = PipelineType.CUSTOM,
    **kwargs: Any,
) -> BasePipeline:
    """Create pipeline instance"""
    config = PipelineConfig(
        name=name,
        pipeline_type=pipeline_type,
        **kwargs
    )
    return BasePipeline(config)
