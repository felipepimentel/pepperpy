"""Embedding models and utilities."""
from typing import List, Dict, Any, Optional
import numpy as np
from abc import ABC, abstractmethod
from .types import EmbeddingModel, Document, TextChunk

class BaseEmbedding(EmbeddingModel):
    """Base class for embedding implementations."""
    
    @abstractmethod
    def embed(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts."""
        pass

class SimpleAverageEmbedding(BaseEmbedding):
    """Simple word vector averaging embedding."""
    
    def __init__(self, word_vectors: Dict[str, np.ndarray]):
        self.word_vectors = word_vectors
        self.vector_size = len(next(iter(word_vectors.values())))
    
    def embed(self, text: str) -> np.ndarray:
        words = text.lower().split()
        vectors = [
            self.word_vectors[word]
            for word in words
            if word in self.word_vectors
        ]
        
        if not vectors:
            return np.zeros(self.vector_size)
        
        return np.mean(vectors, axis=0)
    
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        return [self.embed(text) for text in texts]

class TransformerEmbedding(BaseEmbedding):
    """Transformer-based embedding using sentence-transformers."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
    
    def embed(self, text: str) -> np.ndarray:
        return self.model.encode(text)
    
    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        return self.model.encode(texts)

class EmbeddingPipeline:
    """Pipeline for document embedding."""
    
    def __init__(
        self, 
        embedding_model: EmbeddingModel,
        chunk_embeddings: bool = True
    ):
        self.embedding_model = embedding_model
        self.chunk_embeddings = chunk_embeddings
    
    def process(self, document: Document) -> Document:
        """Process a document and generate embeddings."""
        if self.chunk_embeddings and document.chunks:
            chunk_texts = [chunk.content for chunk in document.chunks]
            embeddings = self.embedding_model.embed_batch(chunk_texts)
            
            for chunk, embedding in zip(document.chunks, embeddings):
                chunk.embedding = embedding
        
        if not self.chunk_embeddings or not document.chunks:
            document.embedding = self.embedding_model.embed(document.content)
        
        return document 