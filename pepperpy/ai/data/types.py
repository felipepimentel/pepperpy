"""Type definitions for data processing module."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union, Protocol
from enum import Enum
import numpy as np

class ChunkingStrategy(Enum):
    """Available chunking strategies."""
    FIXED_SIZE = "fixed_size"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEMANTIC = "semantic"
    OVERLAP = "overlap"

class TextFormat(Enum):
    """Supported text formats."""
    PLAIN = "plain"
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"

@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    content: str
    start_index: int
    end_index: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None

@dataclass
class Document:
    """Represents a document with its content and metadata."""
    content: str
    format: TextFormat
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunks: List[TextChunk] = field(default_factory=list)
    embedding: Optional[np.ndarray] = None

class EmbeddingModel(Protocol):
    """Protocol for embedding models."""
    def embed(self, text: str) -> np.ndarray: ...
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]: ... 