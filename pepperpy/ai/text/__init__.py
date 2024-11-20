"""Text processing module"""

from .analyzer import TextAnalyzer
from .chunker import TextChunker
from .config import TextProcessorConfig
from .epub import EPUBAnalyzer
from .exceptions import (
    AnalysisError,
    ChunkingError,
    ProcessingError,
    TextError,
    TextProcessorError,
)
from .types import TextAnalysisResult, TextChunk

__all__ = [
    # Core
    "TextAnalyzer",
    "TextChunker",
    "EPUBAnalyzer",
    # Config
    "TextProcessorConfig",
    # Types
    "TextAnalysisResult",
    "TextChunk",
    # Exceptions
    "TextError",
    "TextProcessorError",
    "AnalysisError",
    "ChunkingError",
    "ProcessingError",
]
