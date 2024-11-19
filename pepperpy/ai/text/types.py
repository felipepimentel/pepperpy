"""Text processing types"""

from dataclasses import asdict, dataclass, field
from enum import Enum, auto
from typing import Any, AsyncIterator

from pepperpy.core.config import ModuleConfig


class ChunkingStrategy(Enum):
    """Text chunking strategy"""

    TOKENS = auto()
    WORDS = auto()
    SENTENCES = auto()
    PARAGRAPHS = auto()
    SEMANTIC = auto()
    FIXED_SIZE = auto()
    SLIDING_WINDOW = auto()


@dataclass
class TextMetadata:
    """Text metadata"""

    language: str | None = None
    encoding: str | None = None
    source: str | None = None
    created_at: str | None = None
    modified_at: str | None = None
    tokens: int = 0
    sentences: int = 0
    paragraphs: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def update(self, other: dict[str, Any]) -> None:
        """Update metadata"""
        self.metadata.update(other)


@dataclass
class ProcessingConfig(ModuleConfig):
    """Text processing configuration"""

    name: str = "text_processor"
    version: str = "1.0.0"
    clean_whitespace: bool = True
    normalize_unicode: bool = True
    remove_urls: bool = False
    remove_emails: bool = False
    remove_numbers: bool = False
    lowercase: bool = True
    custom_filters: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class ChunkingConfig(ModuleConfig):
    """Text chunking configuration"""

    name: str = "text_chunker"
    version: str = "1.0.0"
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.SENTENCES
    max_chunk_size: int = 1000
    overlap: int = 200
    boundary_chars: list[str] = field(default_factory=lambda: [".", "!", "?"])
    use_tokenizer: bool = False
    tokenizer_model: str = "en_core_web_sm"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class AnalysisConfig(ModuleConfig):
    """Text analysis configuration"""

    name: str = "text_analyzer"
    version: str = "1.0.0"
    model: str = "en_core_web_sm"
    min_concept_frequency: int = 2
    context_window: int = 100
    min_phrase_length: int = 3
    top_phrases: int = 50
    max_keywords: int = 100
    min_keyword_freq: int = 2
    summary_ratio: float = 0.3
    extract_keywords: bool = True
    extract_entities: bool = True
    extract_summary: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class AnalysisResult:
    """Text analysis result"""

    text: str
    summary: str = ""
    keywords: list[str] = field(default_factory=list)
    concepts: list[str] = field(default_factory=list)
    phrases: list[str] = field(default_factory=list)
    entities: dict[str, list[str]] = field(default_factory=dict)
    metadata: TextMetadata = field(default_factory=TextMetadata)


@dataclass
class TextChunk:
    """Text chunk with metadata"""

    text: str
    start_index: int
    end_index: int
    strategy: ChunkingStrategy
    metadata: TextMetadata


__all__ = [
    "ChunkingStrategy",
    "TextMetadata",
    "ProcessingConfig",
    "ChunkingConfig",
    "AnalysisConfig",
    "AnalysisResult",
    "TextChunk",
    "AsyncIterator",
]
