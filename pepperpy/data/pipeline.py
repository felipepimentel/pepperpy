"""Data processing pipeline implementation."""
from typing import List, Optional, Callable
from dataclasses import dataclass, field
from .types import Document, TextFormat, ChunkingStrategy
from .chunking import ChunkingFactory
from .preprocessing import TextPreprocessor
from .embedding import EmbeddingPipeline, EmbeddingModel

@dataclass
class PipelineConfig:
    """Configuration for data processing pipeline."""
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.FIXED_SIZE
    chunking_params: dict = field(default_factory=dict)
    preprocessing_enabled: bool = True
    embedding_enabled: bool = True
    chunk_embeddings: bool = True

# ... resto do código permanece igual ... 