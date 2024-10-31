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

class Pipeline:
    """Configurable data processing pipeline."""
    
    def __init__(
        self,
        config: PipelineConfig,
        embedding_model: Optional[EmbeddingModel] = None,
        preprocessor: Optional[TextPreprocessor] = None
    ):
        self.config = config
        self.preprocessor = preprocessor or TextPreprocessor()
        self.chunker = ChunkingFactory.get_chunker(
            config.chunking_strategy,
            **config.chunking_params
        )
        
        if config.embedding_enabled and embedding_model:
            self.embedding_pipeline = EmbeddingPipeline(
                embedding_model,
                chunk_embeddings=config.chunk_embeddings
            )
        else:
            self.embedding_pipeline = None
    
    def process(self, document: Document) -> Document:
        """Process a document through the pipeline."""
        # Preprocessing
        if self.config.preprocessing_enabled:
            document.content = self.preprocessor.process(document.content)
        
        # Chunking
        document.chunks = self.chunker.chunk(document.content)
        
        # Embedding
        if self.embedding_pipeline:
            document = self.embedding_pipeline.process(document)
        
        return document
    
    def process_batch(self, documents: List[Document]) -> List[Document]:
        """Process multiple documents."""
        return [self.process(doc) for doc in documents] 