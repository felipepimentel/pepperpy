"""Pipeline types and configurations"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from pepperpy.ai.text.types import ProcessingConfig
from pepperpy.ai.text_analysis.types import AnalysisConfig
from pepperpy.core.config import AIConfig, ModuleConfig


class InputType(Enum):
    """Supported input types"""
    EPUB = "epub"
    PDF = "pdf"
    TEXT = "text"
    MARKDOWN = "markdown"
    HTML = "html"


class OutputType(Enum):
    """Supported output types"""
    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"
    TEXT = "text"


@dataclass
class PipelineConfig(ModuleConfig):
    """Configuration for processing pipeline"""
    name: str = "pipeline"
    version: str = "1.0.0"
    input_type: InputType = InputType.EPUB
    output_type: OutputType = OutputType.MARKDOWN
    output_dir: Path = field(default_factory=lambda: Path("pipeline_output"))
    processing_config: ProcessingConfig | None = None
    analysis_config: AnalysisConfig | None = None
    ai_config: AIConfig | None = None
    model: str = "anthropic/claude-3-sonnet"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "input_type": self.input_type.value,
            "output_type": self.output_type.value,
            "output_dir": str(self.output_dir),
            "processing_config": self.processing_config.to_dict() if self.processing_config else None,
            "analysis_config": self.analysis_config.to_dict() if self.analysis_config else None,
            "ai_config": self.ai_config.to_dict() if self.ai_config else None,
            "model": self.model,
            "metadata": self.metadata,
        }


@dataclass
class PipelineResult:
    """Pipeline processing result"""
    output_path: Path
    metadata: dict[str, Any] = field(default_factory=dict) 