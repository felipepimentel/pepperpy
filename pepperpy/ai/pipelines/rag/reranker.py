"""Reranking implementations for RAG."""
from typing import List, Optional
import numpy as np
from dataclasses import dataclass

from ...llm.base import BaseLLM
from ...data.vector.store import SearchResult

@dataclass
class CrossEncoderReRanker:
    """Reranks results using a cross-encoder model."""
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model_name)
        
    async def rerank(
        self,
        query: str,
        results: List[SearchResult]
    ) -> List[SearchResult]:
        """Rerank results using cross-encoder scores."""
        pairs = [(query, result.chunk.content) for result in results]
        scores = self.model.predict(pairs)
        
        # Create new results with updated scores
        reranked = []
        for result, score in zip(results, scores):
            reranked.append(SearchResult(
                chunk=result.chunk,
                document=result.document,
                score=float(score),
                metadata={
                    **result.metadata,
                    "original_score": result.score
                }
            ))
            
        # Sort by new scores
        reranked.sort(key=lambda x: x.score, reverse=True)
        return reranked 