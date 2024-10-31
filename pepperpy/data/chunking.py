"""Text chunking implementations."""
from typing import List, Optional, Dict, Any
import re
from abc import ABC, abstractmethod
from .types import TextChunk, ChunkingStrategy

class BaseChunker(ABC):
    """Base class for text chunking implementations."""
    
    @abstractmethod
    def chunk(self, text: str, **kwargs) -> List[TextChunk]:
        """Split text into chunks."""
        pass

class FixedSizeChunker(BaseChunker):
    """Chunks text into fixed-size pieces."""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str, **kwargs) -> List[TextChunk]:
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Adjust end to not break words
            if end < len(text):
                end = text.rfind(' ', start, end)
                if end == -1:
                    end = start + self.chunk_size
            
            chunks.append(TextChunk(
                content=text[start:end],
                start_index=start,
                end_index=end
            ))
            
            start = end - self.overlap
            
        return chunks

class SentenceChunker(BaseChunker):
    """Chunks text by sentences."""
    
    def __init__(self, max_sentences: int = 5):
        self.max_sentences = max_sentences
        self._sentence_pattern = re.compile(r'(?<=[.!?])\s+')
    
    def chunk(self, text: str, **kwargs) -> List[TextChunk]:
        sentences = self._sentence_pattern.split(text)
        chunks = []
        current_chunk = []
        start_index = 0
        
        for sentence in sentences:
            current_chunk.append(sentence)
            
            if len(current_chunk) >= self.max_sentences:
                content = ' '.join(current_chunk)
                end_index = start_index + len(content)
                chunks.append(TextChunk(
                    content=content,
                    start_index=start_index,
                    end_index=end_index
                ))
                start_index = end_index + 1
                current_chunk = []
        
        if current_chunk:
            content = ' '.join(current_chunk)
            chunks.append(TextChunk(
                content=content,
                start_index=start_index,
                end_index=start_index + len(content)
            ))
        
        return chunks

class ChunkingFactory:
    """Factory for creating chunkers."""
    
    _chunkers = {
        ChunkingStrategy.FIXED_SIZE: FixedSizeChunker,
        ChunkingStrategy.SENTENCE: SentenceChunker,
    }
    
    @classmethod
    def get_chunker(
        cls, 
        strategy: ChunkingStrategy, 
        **kwargs
    ) -> BaseChunker:
        """Get a chunker implementation."""
        if strategy not in cls._chunkers:
            raise ValueError(f"Unsupported chunking strategy: {strategy}")
        return cls._chunkers[strategy](**kwargs) 