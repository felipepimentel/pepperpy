"""Text processor configuration"""

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field


class TextProcessorConfig(BaseModel):
    """Configuration for text processor"""

    model_config = ConfigDict(frozen=True)

    language: str = Field(default="en", description="Default language for text processing")
    min_length: int = Field(default=10, gt=0, description="Minimum text length")
    max_length: int = Field(default=1000, gt=0, description="Maximum text length")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TextAnalyzerConfig(TextProcessorConfig):
    """Configuration for text analyzer"""

    pass


class TextChunkerConfig(TextProcessorConfig):
    """Configuration for text chunker"""

    chunk_size: int = Field(default=500, gt=0, description="Size of each chunk")
    overlap: int = Field(default=50, ge=0, description="Overlap between chunks")
