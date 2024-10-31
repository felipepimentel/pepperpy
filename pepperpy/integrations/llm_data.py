"""Integration between LLM and Data processing capabilities."""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from ..llm import BaseLLM
from ..data.types import Document, TextChunk
from ..data.pipeline import Pipeline, PipelineConfig
from ..data.embedding import EmbeddingModel

@dataclass
class RAGConfig:
    """Configuration for Retrieval-Augmented Generation."""
    chunk_size: int = 1000
    chunk_overlap: int = 100
    similarity_threshold: float = 0.8
    max_chunks: int = 5
    include_metadata: bool = True
    rerank_results: bool = False

class RAGPipeline:
    """Retrieval-Augmented Generation Pipeline."""
    
    def __init__(
        self,
        llm: BaseLLM,
        embedding_model: EmbeddingModel,
        config: Optional[RAGConfig] = None
    ):
        self.llm = llm
        self.config = config or RAGConfig()
        
        # Initialize data pipeline
        pipeline_config = PipelineConfig(
            chunking_strategy="fixed_size",
            chunking_params={
                "chunk_size": self.config.chunk_size,
                "overlap": self.config.chunk_overlap
            },
            embedding_enabled=True,
            chunk_embeddings=True
        )
        self.pipeline = Pipeline(pipeline_config, embedding_model)
        
    async def process_documents(self, documents: List[Document]) -> List[Document]:
        """Process documents through the pipeline."""
        return self.pipeline.process_batch(documents)
        
    async def query(
        self,
        query: str,
        documents: List[Document],
        **kwargs
    ) -> Dict[str, Any]:
        """Query documents using RAG."""
        # Get query embedding
        query_embedding = self.pipeline.embedding_pipeline.embedding_model.embed(query)
        
        # Find relevant chunks
        relevant_chunks = []
        for doc in documents:
            for chunk in doc.chunks:
                if chunk.embedding is None:
                    continue
                    
                similarity = self._calculate_similarity(
                    query_embedding,
                    chunk.embedding
                )
                
                if similarity >= self.config.similarity_threshold:
                    relevant_chunks.append((chunk, similarity, doc.metadata))
        
        # Sort and limit chunks
        relevant_chunks.sort(key=lambda x: x[1], reverse=True)
        relevant_chunks = relevant_chunks[:self.config.max_chunks]
        
        # Build context
        context = self._build_context(relevant_chunks)
        
        # Query LLM
        response = await self.llm.achat(
            messages=[
                {
                    "role": "system",
                    "content": "Use the following context to answer the question.\n\n"
                              f"Context:\n{context}\n\n"
                },
                {"role": "user", "content": query}
            ],
            **kwargs
        )
        
        return {
            "answer": response.content,
            "sources": [
                {
                    "content": chunk.content,
                    "metadata": metadata,
                    "similarity": sim
                }
                for chunk, sim, metadata in relevant_chunks
            ],
            "usage": response.usage,
            "cost": response.cost
        }
        
    def _calculate_similarity(self, embedding1, embedding2) -> float:
        """Calculate cosine similarity between embeddings."""
        from numpy import dot
        from numpy.linalg import norm
        
        return dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))
        
    def _build_context(self, chunks: List[tuple]) -> str:
        """Build context from relevant chunks."""
        context_parts = []
        
        for i, (chunk, similarity, metadata) in enumerate(chunks, 1):
            context_parts.append(f"[{i}] {chunk.content}")
            
            if self.config.include_metadata:
                context_parts.append(f"Source: {metadata}")
                
        return "\n\n".join(context_parts) 