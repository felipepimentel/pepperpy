"""RAG (Retrieval-Augmented Generation) pipeline."""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from ..llm.providers.base import BaseLLM
from ..data.vector.store import VectorStore
from ..memory.vector import VectorMemory
from ..data.preprocessing.chunking import TextChunker

@dataclass
class RAGConfig:
    """RAG pipeline configuration."""
    chunk_size: int = 1000
    chunk_overlap: int = 100
    similarity_threshold: float = 0.7
    max_chunks: int = 5
    include_metadata: bool = True
    use_vector_memory: bool = True

class RAGPipeline:
    """Enhanced RAG implementation."""
    
    def __init__(
        self,
        llm: BaseLLM,
        vector_store: VectorStore,
        config: Optional[RAGConfig] = None,
        memory: Optional[VectorMemory] = None
    ):
        self.llm = llm
        self.vector_store = vector_store
        self.config = config or RAGConfig()
        self.memory = memory if memory and self.config.use_vector_memory else None
        self.chunker = TextChunker(
            chunk_size=self.config.chunk_size,
            overlap=self.config.chunk_overlap
        )
    
    async def query(
        self,
        query: str,
        context: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Query using RAG with optional context."""
        # Get relevant chunks
        chunks = await self._get_relevant_chunks(query)
        
        # Build context
        full_context = self._build_context(chunks, additional_context=context)
        
        # Query LLM
        response = await self.llm.achat(
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_prompt(full_context)
                },
                {"role": "user", "content": query}
            ],
            **kwargs
        )
        
        # Update memory if enabled
        if self.memory:
            await self.memory.add_interaction(
                query=query,
                response=response.content,
                chunks=chunks
            )
        
        return {
            "answer": response.content,
            "sources": self._format_sources(chunks),
            "usage": response.usage,
            "cost": response.cost
        }
    
    # ... métodos auxiliares ... 