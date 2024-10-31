"""Vector store implementations for semantic search."""
from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
import numpy as np
from dataclasses import dataclass
from .types import TextChunk, Document

@dataclass
class SearchResult:
    """Represents a vector search result."""
    chunk: TextChunk
    document: Document
    score: float
    metadata: Dict[str, Any]

class VectorStore(ABC):
    """Abstract base class for vector stores."""
    
    @abstractmethod
    async def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the store."""
        pass
    
    @abstractmethod
    async def search(
        self,
        query_vector: np.ndarray,
        limit: int = 5,
        score_threshold: float = 0.0
    ) -> List[SearchResult]:
        """Search for similar vectors."""
        pass
    
    @abstractmethod
    async def delete(self, document_ids: List[str]) -> None:
        """Delete documents from the store."""
        pass

class InMemoryVectorStore(VectorStore):
    """Simple in-memory vector store using numpy."""
    
    def __init__(self):
        self.vectors: List[np.ndarray] = []
        self.chunks: List[TextChunk] = []
        self.documents: List[Document] = []
        
    async def add_documents(self, documents: List[Document]) -> None:
        for doc in documents:
            for chunk in doc.chunks:
                if chunk.embedding is not None:
                    self.vectors.append(chunk.embedding)
                    self.chunks.append(chunk)
                    self.documents.append(doc)
    
    async def search(
        self,
        query_vector: np.ndarray,
        limit: int = 5,
        score_threshold: float = 0.0
    ) -> List[SearchResult]:
        if not self.vectors:
            return []
            
        # Convert to numpy array for efficient computation
        vectors = np.array(self.vectors)
        
        # Compute cosine similarities
        similarities = np.dot(vectors, query_vector) / (
            np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_vector)
        )
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:limit]
        
        results = []
        for idx in top_indices:
            score = similarities[idx]
            if score < score_threshold:
                continue
                
            results.append(SearchResult(
                chunk=self.chunks[idx],
                document=self.documents[idx],
                score=float(score),
                metadata={
                    "index": idx,
                    "document_id": id(self.documents[idx])
                }
            ))
            
        return results
    
    async def delete(self, document_ids: List[str]) -> None:
        # Convert document_ids to set for O(1) lookup
        id_set = set(document_ids)
        
        # Filter out deleted documents
        indices_to_keep = [
            i for i, doc in enumerate(self.documents)
            if str(id(doc)) not in id_set
        ]
        
        if not indices_to_keep:
            self.vectors = []
            self.chunks = []
            self.documents = []
            return
            
        self.vectors = [self.vectors[i] for i in indices_to_keep]
        self.chunks = [self.chunks[i] for i in indices_to_keep]
        self.documents = [self.documents[i] for i in indices_to_keep] 