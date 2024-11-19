"""Text processing and analysis module"""

from .analyzer import TextAnalyzer
from .chunker import TextChunker
from .exceptions import (
    AnalysisError,
    ChunkingError,
    ProcessingError,
    TextError,
)
from .processor import TextProcessor
from .types import (
    AnalysisConfig,
    AnalysisResult,
    ChunkingConfig,
    ChunkingStrategy,
    ProcessingConfig,
    TextChunk,
    TextMetadata,
)

__all__ = [
    # Core classes
    "TextAnalyzer",
    "TextChunker",
    "TextProcessor",
    # Configurations
    "AnalysisConfig",
    "ChunkingConfig",
    "ProcessingConfig",
    # Types
    "AnalysisResult",
    "ChunkingStrategy",
    "TextChunk",
    "TextMetadata",
    # Exceptions
    "TextError",
    "AnalysisError",
    "ChunkingError",
    "ProcessingError",
]
