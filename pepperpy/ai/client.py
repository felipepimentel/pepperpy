"""AI client implementation"""

from typing import Any, AsyncGenerator

from .config import AIConfig
from .exceptions import AIError
from .types import AIResponse
from .vector import VectorConfig, VectorManager


class AIClient:
    """AI operations client"""

    def __init__(self, config: AIConfig, vector_config: VectorConfig | None = None) -> None:
        self.config = config
        self._vector_manager = None
        if vector_config:
            self._vector_manager = VectorManager(vector_config, self)

    async def initialize(self) -> None:
        """Initialize AI client"""
        if self._vector_manager:
            await self._vector_manager.initialize()

    async def complete(self, prompt: str) -> AIResponse:
        """Complete text using AI model"""
        try:
            # Implementation depends on the AI provider
            raise NotImplementedError
        except Exception as e:
            raise AIError(f"Completion failed: {e}", cause=e)

    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream completion results"""
        try:
            # Implementation depends on the AI provider
            raise NotImplementedError
            yield ""  # Added to satisfy AsyncGenerator type
        except Exception as e:
            raise AIError(f"Stream completion failed: {e}", cause=e)

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        try:
            # Implementation depends on the AI provider
            raise NotImplementedError
        except Exception as e:
            raise AIError(f"Failed to get embedding: {e}", cause=e)

    async def store_embedding(
        self, collection: str, text: str, metadata: dict[str, Any] | None = None
    ) -> int:
        """Store text embedding"""
        if not self._vector_manager:
            raise AIError("Vector manager not configured")

        try:
            embedding = await self.get_embedding(text)
            [vector_id] = await self._vector_manager.store_vectors(
                collection, [embedding], [metadata] if metadata else None
            )
            return vector_id
        except Exception as e:
            raise AIError(f"Failed to store embedding: {e}", cause=e)

    async def find_similar(
        self, collection: str, text: str, limit: int = 10, threshold: float = 0.8
    ) -> list[dict[str, Any]]:
        """Find similar texts by embedding"""
        if not self._vector_manager:
            raise AIError("Vector manager not configured")

        try:
            query_embedding = await self.get_embedding(text)
            results = await self._vector_manager.search_similar(
                collection, query_embedding, limit=limit, threshold=threshold
            )
            return [
                {"id": r.id, "similarity": r.similarity, "metadata": r.metadata} for r in results
            ]
        except Exception as e:
            raise AIError(f"Similarity search failed: {e}", cause=e)
