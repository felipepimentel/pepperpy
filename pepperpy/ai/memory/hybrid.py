"""Hybrid memory system combining conversation and vector memory."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np

from .conversation import ConversationMemory
from ..data.vector.store import VectorStore, SearchResult

@dataclass
class HybridMemoryConfig:
    """Configuration for hybrid memory."""
    max_conversation_messages: int = 10
    relevance_threshold: float = 0.7
    max_relevant_memories: int = 3
    include_metadata: bool = True

class HybridMemory:
    """Combines conversation and vector memory for enhanced context."""
    
    def __init__(
        self,
        vector_store: VectorStore,
        config: Optional[HybridMemoryConfig] = None
    ):
        self.vector_store = vector_store
        self.config = config or HybridMemoryConfig()
        self.conversation = ConversationMemory(
            max_messages=self.config.max_conversation_messages
        )
        
    async def add_memory(
        self,
        content: str,
        embedding: np.ndarray,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a memory to both stores."""
        # Add to conversation if recent
        if len(self.conversation.messages) < self.config.max_conversation_messages:
            self.conversation.add_message("memory", content, metadata)
            
        # Add to vector store
        await self.vector_store.add_memory(content, embedding, metadata)
        
    async def get_relevant_context(
        self,
        query_embedding: np.ndarray,
        current_conversation: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Get relevant context combining both memory types."""
        # Get relevant memories from vector store
        vector_results = await self.vector_store.search(
            query_embedding,
            limit=self.config.max_relevant_memories,
            score_threshold=self.config.relevance_threshold
        )
        
        # Get conversation context
        conversation_context = (
            current_conversation or 
            self.conversation.get_context(include_metadata=self.config.include_metadata)
        )
        
        return {
            "conversation": conversation_context,
            "relevant_memories": [
                {
                    "content": result.chunk.content,
                    "score": result.score,
                    "metadata": result.metadata
                }
                for result in vector_results
            ]
        } 